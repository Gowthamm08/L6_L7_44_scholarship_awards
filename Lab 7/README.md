# Lab 7: Fuzzing for Input Validation Bugs

**Student:** Gowtham B.  
**SRN:** PES1UG24CS172  
**GitHub:** [Gowthamm08](https://github.com/Gowthamm08)

## Objective

Use Hypothesis property-based tests to explore ordinary and malformed inputs for the scholarship processor, find validation bugs, and improve the functions so malformed input raises a clear `ValueError`.

## Application and functions

`processor.py` contains:

- `parse_applicant(text)`: parses a `category:marks` record.
- `marks_average(marks_csv)`: returns the floor average of comma-separated integer marks.
- `payable_award(text)`: applies an 18% increase, subtracts a deduction, and clamps the result to zero.

Decimals remain valid for applicant marks and payable awards, as in the original implementation. No maximum mark or currency limit has been added.

## Fuzzing approach

Tests in `test_processor.py` combine explicit pytest boundary cases with Hypothesis-generated text, `None`, integers, floats, lists, and sampled categories. The three arbitrary-input properties each explore up to 300 examples. Positive-value properties check actual results and the preserved calculation rules. Invalid values must raise `ValueError`; unexpected exception types fail the tests.

## Bugs found and fixes

The original implementation raised `AttributeError` for non-text inputs; Hypothesis minimized this to `None` for each function. The parser also accepted empty categories, negative and non-finite marks. The average accepted negative marks. Award calculation accepted negative and non-finite values and could produce infinity. `main()` stopped at the first invalid prompt.

The fixed functions validate text types, delimiters, required fields, numeric conversion, nonnegative values, and finite floating-point values. The award calculation checks its result for overflow. The interactive program reports invalid input and continues through the remaining prompts.

## Results

- Original implementation: 46 pytest cases, **20 failed and 26 passed**. Failures include the minimized input `None` and accepted invalid values such as `:82`, `merit:NaN`, `-1,2`, and `NaN|0`.
- Fixed implementation: **50 passed** with `python -m pytest -v test_processor.py`.
- Line coverage: **99%** (74 statements; the remaining line is the script entry-point guard).
- Hypothesis: 6.170.17. pytest: 8.3.4. Python: 3.11.9.

## Commands

Install the required packages:

```powershell
python -m pip install hypothesis pytest
```

Verify dependencies and run tests from `Lab 7/`:

```powershell
python -m pip show hypothesis
python -m pytest --version
python processor.py
python -m pytest -v test_processor.py
```

Optional line coverage check:

```powershell
python -m pytest -v --cov=processor --cov-report=term-missing test_processor.py
```

## Evidence and deliverables

- `screenshots/01_dependencies.txt`, `02_original_application.txt`, `03_initial_fuzz_failures.txt`, `04_fixed_application.txt`, and `05_final_fuzz_tests.txt` are unedited terminal output captured from real runs.
- The requested PNG screenshots are not included because the environment does not permit automated control of Windows Terminal. `screenshots/README.md` gives manual capture instructions and the expected PNG filenames. No synthetic screenshots are presented as evidence.
- `coverage_results.txt` contains the measured code coverage output.
- `Lab7_FuzzTesting_Report_PES1UG24CS172.pdf` is the formatted laboratory report.

## Conclusion

Hypothesis exposed malformed inputs that were accepted or caused uncaught errors. The implementation now preserves the original valid calculations while rejecting malformed and non-finite input consistently. All 50 final tests pass.
