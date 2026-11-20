import pytest
from scholarship_awards import award_amount, is_eligible, application_status


@pytest.mark.parametrize("category, cutoff", [("merit", 75), ("sports", 60), ("arts", 65)])
def test_categories_cutoff_boundaries(category, cutoff):
    assert award_amount(category, cutoff - 1, "low", False) == 0
    assert award_amount(category, cutoff, "low", False) == 0
    assert award_amount(category, cutoff + 1, "low", False) == 100


def test_award_validation():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("science", 90, "low", False)
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -1, "low", False)


@pytest.mark.parametrize("category", ["merit", "arts"])
def test_non_sports_renewal_reduces_cutoff(category):
    cutoff = {"merit": 75, "arts": 65}[category]
    assert award_amount(category, cutoff - 4, "low", True) == 100
    assert award_amount(category, cutoff - 5, "low", True) == 0


def test_sports_renewal_does_not_reduce_cutoff():
    assert award_amount("sports", 55, "low", True) == 0
    assert award_amount("sports", 61, "low", True) == 100


@pytest.mark.parametrize("income, rate", [("low", 100), ("middle", 60), ("high", 60)])
def test_award_income_rates(income, rate):
    assert award_amount("merit", 80, income, False) == 5 * rate


def test_above_fifteen_rate_branches():
    assert award_amount("merit", 90, "middle", False) == 15 * 60
    assert award_amount("merit", 91, "middle", False) == 16 * 100
    assert award_amount("merit", 91, "low", False) == 16 * 160


@pytest.mark.parametrize("attendance, backlogs, expected", [(75, 1, True), (90, 0, True), (74, 0, False), (90, 2, False), (75, 2, False)])
def test_normal_eligibility(attendance, backlogs, expected):
    assert is_eligible(attendance, backlogs, False) is expected


@pytest.mark.parametrize("backlogs, expected", [(0, True), (1, True), (2, True), (3, False)])
def test_special_quota_eligibility(backlogs, expected):
    assert is_eligible(0, backlogs, True) is expected


@pytest.mark.parametrize("days, renewal, paper, expected", [
    (20, False, False, "open"), (35, True, False, "open"),
    (30, False, True, "open"), (40, True, True, "open"),
    (19, False, False, "closing"), (5, False, False, "closing"),
    (4, False, False, "closed"), (14, True, False, "closed"),
    (15, True, False, "closing"), (14, False, True, "closed"),
    (25, True, True, "closing"), (24, True, True, "closed"), (3, True, True, "closed"),
])
def test_application_status(days, renewal, paper, expected):
    assert application_status(days, renewal, paper) == expected

