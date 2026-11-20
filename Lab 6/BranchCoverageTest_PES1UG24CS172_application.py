"""Independent decision/branch coverage tests for scholarship_awards."""
import pytest
from scholarship_awards import award_amount, is_eligible, application_status


# Category validation: invalid category branch and accepted category branch.
def test_category_validation_branches():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("unknown", 80, "low", False)
    assert award_amount("merit", 75, "low", False) == 0


# Negative-mark validation: negative and nonnegative branches.
def test_negative_marks_branches():
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -1, "low", False)
    assert award_amount("merit", 0, "low", False) == 0


# Renewal and non-sports condition: all decision combinations.
@pytest.mark.parametrize("category, renewal, marks, expected", [
    ("merit", True, 70, 0), ("merit", False, 70, 0),
    ("sports", True, 55, 0), ("arts", True, 61, 100),
])
def test_renewal_adjustment_branches(category, renewal, marks, expected):
    assert award_amount(category, marks, "low", renewal) == expected


# Above-cutoff decision: zero-award branch and positive-award branch.
def test_above_cutoff_branches():
    assert award_amount("merit", 75, "low", False) == 0
    assert award_amount("merit", 76, "low", False) == 100


# Income condition: low income and all other income levels.
def test_income_rate_branches():
    assert award_amount("merit", 80, "low", False) == 500
    assert award_amount("merit", 80, "middle", False) == 300


# Above-15 condition and nested low-income rate increase.
def test_above_fifteen_and_nested_income_branches():
    assert award_amount("merit", 90, "middle", False) == 900
    assert award_amount("merit", 91, "middle", False) == 1600
    assert award_amount("merit", 91, "low", False) == 2560


# Special quota: true and false decisions; quota bypasses attendance checks.
def test_special_quota_branch():
    assert is_eligible(0, 2, True) is True
    assert is_eligible(0, 3, True) is False
    assert is_eligible(100, 0, False) is True


# Attendance condition: below 75 returns immediately; 75 continues.
def test_attendance_branches():
    assert is_eligible(74, 0, False) is False
    assert is_eligible(75, 0, False) is True


# Backlog condition in ordinary and special quota paths.
def test_backlog_branches():
    assert is_eligible(75, 1, False) is True
    assert is_eligible(75, 2, False) is False
    assert is_eligible(0, 0, True) is True
    assert is_eligible(0, 1, True) is True
    assert is_eligible(0, 2, True) is True
    assert is_eligible(0, 3, True) is False


# Renewal and paper cutoff decisions each take both outcomes.
def test_renewal_and_paper_status_branches():
    assert application_status(20, False, False) == "open"
    assert application_status(30, False, True) == "open"
    assert application_status(35, True, False) == "open"
    assert application_status(40, True, True) == "open"
    assert application_status(15, True, False) == "closing"
    assert application_status(25, True, True) == "closing"


# Open, closing, and closed decision boundaries.
def test_status_boundaries():
    assert application_status(20, False, False) == "open"
    assert application_status(19, False, False) == "closing"
    assert application_status(5, False, False) == "closing"
    assert application_status(4, False, False) == "closed"
    assert application_status(35, True, False) == "open"
    assert application_status(15, True, False) == "closing"
    assert application_status(15, True, False) == "closing"
    assert application_status(25, True, True) == "closing"
    assert application_status(3, True, True) == "closed"

