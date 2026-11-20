"""Independent line coverage tests for scholarship_awards."""
import pytest
from scholarship_awards import award_amount, is_eligible, application_status


def test_award_amount_executable_lines():
    for category, cutoff in [("merit", 75), ("sports", 60), ("arts", 65)]:
        assert award_amount(category, cutoff, "low", False) == 0
        assert award_amount(category, cutoff + 1, "low", False) == 100
    assert award_amount("merit", 70, "low", True) == 0
    assert award_amount("merit", 71, "low", True) == 100
    assert award_amount("sports", 61, "low", True) == 100
    assert award_amount("merit", 91, "low", False) == 2560
    assert award_amount("merit", 91, "other", False) == 1600
    with pytest.raises(ValueError):
        award_amount("unknown", 80, "low", False)
    with pytest.raises(ValueError):
        award_amount("merit", -1, "low", False)


def test_eligibility_executable_lines():
    assert is_eligible(75, 1, False)
    assert not is_eligible(74, 0, False)
    assert not is_eligible(90, 2, False)
    assert is_eligible(0, 2, True)
    assert not is_eligible(90, 3, True)


def test_application_status_executable_lines():
    assert application_status(20, False, False) == "open"
    assert application_status(5, False, False) == "closing"
    assert application_status(4, False, False) == "closed"
    assert application_status(35, True, False) == "open"
    assert application_status(40, True, True) == "open"
    assert application_status(15, True, False) == "closing"
    assert application_status(25, True, True) == "closing"

