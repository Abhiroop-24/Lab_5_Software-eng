# Issue Documentation Table

**Course:** Software Engineering Lab (UE24CS351A / UE24CS352A)  
**Lab Assignment:** Lab 5 — Static Code Analysis  
**Student Name:** Abhiroop  
**SRN:** PES2UG24CS024  
**Target Repository:** [wildlife_sightings.py](file:///c:/Users/abhiroop/Documents/SE/Lab_5/reference_repo/wildlife_sightings.py)

---

## Static Analysis Issues and Resolutions

| Issue | Tool | Severity / Code | Line(s) | Description | Fix Approach |
|-------|------|-----------------|---------|-------------|--------------|
| **SQL Injection Vulnerability** | Bandit | Medium (`B608`) / `CWE-89` | 9 | String formatting (`.format()`) used to construct SQL `INSERT` statement, creating a major SQL injection vulnerability if untrusted inputs are passed. | Replaced string interpolation with parameterized queries using SQLite placeholder syntax `VALUES (?, ?, ?)` passing values as a tuple. |
| **Insecure Cryptographic Hash** | Bandit | High (`B324`) / `CWE-327` | 15 | Use of weak MD5 hash function (`hashlib.md5`) without explicitly specifying that it is not being used for cryptographically sensitive operations. | Added `usedforsecurity=False` parameter to `hashlib.md5()` call to explicitly mark it for non-security checksum / ID generation purposes. |
| **Use of Assert in Production Code** | Bandit | Low (`B101`) / `CWE-703` | 36 | `assert` statement used for flow validation. Assert statements are removed when Python compiles with optimizations (`-O`), bypassing checks. | Replaced `assert len(totals) == 3` with an explicit conditional check that raises `ValueError("Expected 3 distinct species in totals")`. |
| **Line Length Exceeds Limit** | Flake8 / Pylint | Style (`E501` / `C0301`) | 5, 9, 19, 27 | Multiple lines exceeded the PEP 8 standard maximum line length of 79 characters (up to 117 characters). | Reformatted multiline SQL query strings and statements into cleanly formatted multiline blocks conforming strictly to PEP 8 (<79 characters). |
| **Ambiguous Variable Name** | Flake8 | Style (`E741`) | 28 | Single-letter variable name `l` assigned to the minimum record; easily confused with the numeral `1` or uppercase `I`. | Renamed variable `l` to descriptive name `min_record`. |
| **Missing Whitespace Around Operator** | Flake8 | Style (`E225`) | 28 | Missing spaces surrounding the assignment operator (`l=min(...)`). | Added standard single space before and after the `=` operator (`min_record = min(...)`). |
| **Mutable Default Argument** | Pylint | Warning (`W0102`) | 8 | Function `logSighting` defined default dictionary `extras={}` which is mutated across function invocations, causing state leak between calls. | Changed default value to `extras=None` and initialized `extras = {}` inside the function body if `extras is None`. |
| **Invalid Function & Identifier Naming** | Pylint | Convention (`C0103`) | 8, 14, 18 | Function names `logSighting`, `observerId`, and `zoneSummary` violated PEP 8 `snake_case` naming conventions. | Renamed functions to `log_sighting`, `observer_id`, and `zone_summary`. |
| **Variable Shadowing / Outer Scope Redefinition** | Pylint | Warning (`W0621`) | 8, 18, 26 | Global variable `conn` was redefined as an argument name `conn` in multiple functions (`redefined-outer-name`). | Moved global `conn` instantiation inside `main()` and renamed function parameters to `connection`. |
| **Missing Module & Function Docstrings** | Pylint | Convention (`C0114`, `C0116`) | 1, 8, 14, 18, 26, 32 | Missing docstrings explaining the purpose and arguments of the module and all functions. | Added comprehensive PEP 257 docstrings for the module and all functions (`log_sighting`, `observer_id`, `zone_summary`, `rarest`, `main`). |
| **Unnecessary Else Statement** | Pylint | Refactor (`R1705`) | 20-23 | Unnecessary `else` block after `return` statement (`no-else-return`). | Removed redundant `else:` block and unindented the second `return` statement. |

---

## Tool Summary Comparison

| Tool | Before Fixes | After Fixes | Status |
|------|--------------|-------------|--------|
| **Bandit** | 3 issues (1 High, 1 Medium, 1 Low) | 0 issues | **Clean (Zero issues)** |
| **Flake8** | 6 style errors (4x `E501`, 1x `E741`, 1x `E225`) | 0 errors | **Clean (Zero violations)** |
| **Pylint** | Score: 3.46 / 10 | Score: 10.00 / 10 | **Perfect Score (10.00 / 10)** |

