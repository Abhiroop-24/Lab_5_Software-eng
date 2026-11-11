"""Module for logging and analyzing wildlife sanctuary sightings."""
import hashlib
import sqlite3


def log_sighting(connection, species, zone, count, extras=None):
    """Log a wildlife sighting into the database and update species count."""
    if extras is None:
        extras = {}
    query = """
        INSERT INTO sightings (species, zone, count)
        VALUES (?, ?, ?)
    """
    connection.execute(query, (species, zone, count))
    extras[species] = extras.get(species, 0) + count
    return extras


def observer_id(observer):
    """Generate a short identifier for an observer using MD5 hash."""
    digest = hashlib.md5(
        observer.encode(), usedforsecurity=False
    ).hexdigest()
    return digest[:6]


def zone_summary(connection, zone):
    """Calculate total animal count observed in a specific zone."""
    query = """
        SELECT SUM(count) FROM sightings WHERE zone = ?
    """
    row = connection.execute(query, (zone,)).fetchone()
    if row[0] is None:
        return 0
    return row[0]


def rarest(connection):
    """Identify the species with the lowest total observed count."""
    query = """
        SELECT species, SUM(count) FROM sightings GROUP BY species
    """
    rows = connection.execute(query).fetchall()
    min_record = min(rows, key=lambda r: r[1])
    return min_record[0]


def main():
    """Main function to demonstrate wildlife sightings logging."""
    conn = sqlite3.connect(":memory:")
    table_schema = """
        CREATE TABLE sightings (
            id INTEGER PRIMARY KEY,
            species TEXT,
            zone TEXT,
            count INTEGER
        )
    """
    conn.execute(table_schema)

    totals = log_sighting(conn, "Leopard", "North", 1)
    log_sighting(conn, "Chital", "North", 24, totals)
    log_sighting(conn, "Hornbill", "East", 3, totals)
    if len(totals) != 3:
        raise ValueError("Expected 3 distinct species in totals")
    print(observer_id("Arun"), zone_summary(conn, "North"), rarest(conn))


if __name__ == "__main__":
    main()
