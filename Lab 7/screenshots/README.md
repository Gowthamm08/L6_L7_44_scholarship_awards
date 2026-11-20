# Manual terminal screenshots

This environment cannot automate Windows Terminal, so the five PNG screenshots are not generated here. The text files beside this README are genuine, unedited terminal output from the corresponding runs. Use Snipping Tool to capture the visible terminal and save PNGs in this directory with the names below. Do not alter the displayed output.

1. `01_dependencies.png`: in `Lab 7`, run `python -m pip show hypothesis` and `python -m pytest --version`.
2. `02_original_application.png`: display the saved original run using `Get-Content screenshots/02_original_application.txt`.
3. `03_initial_fuzz_failures.png`: display `Get-Content screenshots/03_initial_fuzz_failures.txt`; the original failures were run against the unmodified application before the fixes.
4. `04_fixed_application.png`: display `Get-Content screenshots/04_fixed_application.txt`.
5. `05_final_fuzz_tests.png`: run `python -m pytest -v test_processor.py` and capture the successful result.

Supporting actual outputs are `01_dependencies.txt`, `01_dependencies_pytest.txt`, `02_original_application.txt`, `03_initial_fuzz_failures.txt`, `04_fixed_application.txt`, and `05_final_fuzz_tests.txt`.
