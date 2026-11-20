# Lab 6: Code and Branch Coverage Analysis

**Student:** Gowtham B.  
**SRN:** PES1UG24CS172  
**GitHub:** [Gowthamm08](https://github.com/Gowthamm08)

## Objective

Test the scholarship award application with pytest and measure how much of its executable code and decision branches are exercised.

## Coverage concepts

Code (line) coverage measures the executable lines run by the tests. Branch coverage also checks the possible outcomes of decisions, such as true and false sides of an `if` statement. A program can have high line coverage while still missing a decision outcome, so branch coverage gives a more complete view of conditional behavior.

## Functions tested

- `award_amount(category, marks, income_level, is_renewal)`: input validation, category cutoffs, renewal rules, income rates, and award rate boundaries.
- `is_eligible(attendance, backlogs, is_special_quota)`: normal attendance and backlog rules, special quota limits, and quota attendance bypass.
- `application_status(days_left, is_renewal, is_paper)`: normal and renewal deadlines, paper deadline adjustment, and open/closing/closed boundaries.

## Tools and commands

Tested with Python 3.11.9, pytest 8.3.4, pytest-cov 7.1.0, and coverage 7.17.3.

Install dependencies:

```powershell
python -m pip install pytest pytest-cov coverage
```

Run starter/comprehensive tests:

```powershell
python -m pytest test_scholarship_awards.py
```

Run line coverage:

```powershell
python -m pytest --cov=scholarship_awards --cov-report=term-missing CodeCoverageTest_PES1UG24CS172_application.py
```

Run branch coverage:

```powershell
python -m pytest --cov=scholarship_awards --cov-branch --cov-report=term-missing BranchCoverageTest_PES1UG24CS172_application.py
```

Run all three suites together:

```powershell
python -m pytest test_scholarship_awards.py CodeCoverageTest_PES1UG24CS172_application.py BranchCoverageTest_PES1UG24CS172_application.py
```

## Measured results

- Code coverage suite: **100% line coverage** (37 statements, 0 missing); 3 tests passed.
- Branch coverage suite: **100% coverage** (37 statements, all 26 branch paths covered, 0 partial); 14 tests passed.
- Missing lines or branches: **none** in the dedicated coverage runs.
- Comprehensive starter suite: 33 parametrized and standalone cases.

Full terminal output is saved in `coverage_reports/code_coverage.txt` and `coverage_reports/branch_coverage.txt`.

## Evidence screenshots

The `screenshots/` directory contains terminal captures for code coverage execution and report, branch coverage execution and report, and final successful test results.

## Conclusion

The three scholarship functions are tested across valid and invalid inputs, boundary values, and both outcomes of the measured conditional branches. The dedicated runs achieved 100% line and branch coverage, and the tests passed.

