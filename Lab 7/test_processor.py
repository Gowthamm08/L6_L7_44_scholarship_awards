import math
import pytest
from hypothesis import given, settings, strategies as st
from processor import parse_applicant, marks_average, payable_award

VALID_CATEGORIES = st.sampled_from(["merit", "sports", "arts", "Other"])
FINITE_NONNEGATIVE = st.floats(min_value=0, max_value=1_000_000, allow_nan=False, allow_infinity=False)
ARBITRARY_INPUT = st.one_of(st.text(), st.none(), st.integers(), st.floats(allow_nan=True, allow_infinity=True))

@given(VALID_CATEGORIES, FINITE_NONNEGATIVE)
def test_parse_applicant_valid_records(category, marks):
    assert parse_applicant(f"{category}:{marks}") == (category.title(), marks)

@pytest.mark.parametrize("text, expected", [("merit:82.5", ("Merit", 82.5)), ("  arts : 65  ", ("Arts", 65.0)), ("mérit:82", ("Mérit", 82.0))])
def test_parse_applicant_decimal_whitespace_and_unicode(text, expected):
    assert parse_applicant(text) == expected


def test_parse_applicant_very_long_category():
    category = "a" * 10_000
    assert parse_applicant(f"{category}:1") == (category.title(), 1.0)

@pytest.mark.parametrize("text", ["", ":82", "merit:", "merit", "merit:82:extra", "merit:abc", "merit:NaN", "merit:inf", "   :82", "merit:-1"])
def test_parse_applicant_rejects_malformed_records(text):
    with pytest.raises(ValueError):
        parse_applicant(text)

@given(ARBITRARY_INPUT)
@settings(max_examples=300)
def test_parse_applicant_arbitrary_inputs_are_valid_or_raise_value_error(value):
    try:
        result = parse_applicant(value)
    except ValueError:
        return
    assert isinstance(value, str), "non-text input was accepted"
    assert value.count(":") == 1, "malformed delimiter count was accepted"
    category, raw_marks = value.split(":")
    assert category.strip(), "empty category was accepted"
    expected_marks = float(raw_marks.strip())
    assert math.isfinite(expected_marks) and expected_marks >= 0
    assert result == (category.strip().title(), expected_marks)

@given(st.lists(st.integers(min_value=0), min_size=1, max_size=50))
def test_marks_average_valid_lists_have_floor_average(values):
    text = ",".join(str(value) for value in values)
    assert marks_average(text) == sum(values) // len(values)

def test_marks_average_large_and_unicode_integers():
    large_value = 10**100
    assert marks_average(f"{large_value},0") == large_value // 2
    assert marks_average("٨,٢") == 5
    assert marks_average(",".join(["1"] * 1_000)) == 1

@pytest.mark.parametrize("text", ["", ",", "1,", ",1", "1,,2", "one,2", "1.5,2", "-1,2", "  ,  "])
def test_marks_average_rejects_malformed_csv(text):
    with pytest.raises(ValueError):
        marks_average(text)

@given(ARBITRARY_INPUT)
@settings(max_examples=300)
def test_marks_average_arbitrary_inputs_are_valid_or_raise_value_error(value):
    try:
        result = marks_average(value)
    except ValueError:
        return
    assert isinstance(value, str), "non-text input was accepted"
    fields = value.split(",")
    assert fields and all(field.strip() for field in fields), "empty CSV element was accepted"
    values = [int(field.strip()) for field in fields]
    assert all(number >= 0 for number in values), "negative mark was accepted"
    assert result == sum(values) // len(values)

@given(FINITE_NONNEGATIVE, FINITE_NONNEGATIVE)
def test_payable_award_valid_values_preserve_eighteen_percent_rule(award, deduction):
    actual = payable_award(f"{award}|{deduction}")
    expected = max(award * 1.18 - deduction, 0)
    assert actual == pytest.approx(expected)
    assert math.isfinite(actual) and actual >= 0

def test_payable_award_accepts_decimal_and_large_finite_values():
    assert payable_award("1.5|0.25") == pytest.approx(1.52)
    assert payable_award("1e100|0") == pytest.approx(1e100 * 1.18)

@pytest.mark.parametrize("text", ["", "500", "|1", "1|", "500|1|2", "x|1", "1|x", "NaN|0", "inf|0", "-1|0", "1|-1", "1.7e308|0"])
def test_payable_award_rejects_malformed_values(text):
    with pytest.raises(ValueError):
        payable_award(text)

@given(ARBITRARY_INPUT)
@settings(max_examples=300)
def test_payable_award_arbitrary_inputs_are_valid_or_raise_value_error(value):
    try:
        result = payable_award(value)
    except ValueError:
        return
    assert isinstance(value, str), "non-text input was accepted"
    assert value.count("|") == 1, "malformed separator count was accepted"
    raw_award, raw_deduction = value.split("|")
    award = float(raw_award.strip())
    deduction = float(raw_deduction.strip())
    assert math.isfinite(award) and math.isfinite(deduction)
    assert award >= 0 and deduction >= 0
    expected = max(award * 1.18 - deduction, 0)
    assert math.isfinite(result) and result >= 0
    assert result == pytest.approx(expected)

@pytest.mark.parametrize("value", [None, 10, 2.5, [], {}, True])
def test_all_functions_reject_unexpected_types(value):
    for function in (parse_applicant, marks_average, payable_award):
        with pytest.raises(ValueError):
            function(value)


def test_main_reports_invalid_input_and_continues(monkeypatch, capsys):
    answers = iter(["merit:NaN", "72,85,90", "5000|500"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    from processor import main

    main()
    output = capsys.readouterr().out
    assert "Invalid input: marks must be finite" in output
    assert "Average Marks: 82" in output
    assert "Payable Award: 5400.0" in output
