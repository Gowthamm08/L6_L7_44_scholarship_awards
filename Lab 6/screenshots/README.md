# Screenshot capture instructions

This folder is ready for the five requested terminal screenshots. The current computer-use tooling does not permit automating Windows Terminal, PowerShell, or Command Prompt, so no terminal screenshot has been fabricated.

From `Lab 6`, open a terminal and run each command below. Arrange the terminal so the command and its real output are visible, then use Windows Snipping Tool to save the capture using the listed filename.

1. `python -m pytest --cov=scholarship_awards --cov-report=term-missing CodeCoverageTest_PES1UG24CS172_application.py` → `code_coverage_execution.png`
2. Capture the resulting table containing `100%` line coverage → `code_coverage_report.png`
3. `python -m pytest --cov=scholarship_awards --cov-branch --cov-report=term-missing BranchCoverageTest_PES1UG24CS172_application.py` → `branch_coverage_execution.png`
4. Capture the resulting table containing 100% coverage and `26` branches with `0` partial → `branch_coverage_report.png`
5. `python -m pytest test_scholarship_awards.py CodeCoverageTest_PES1UG24CS172_application.py BranchCoverageTest_PES1UG24CS172_application.py` → `final_test_results.png`

Save all PNG files in this directory. The exact executed outputs are also preserved as text in `../coverage_reports/`.
