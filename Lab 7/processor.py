"""Input parsing and award calculations for the Lab 7 fuzzing exercise."""
import math


def _require_text(value, field_name):
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be text")
    if not value.strip():
        raise ValueError(f"{field_name} cannot be empty")


def parse_applicant(text):
    """Parse 'category:marks'; marks must be finite and nonnegative."""
    _require_text(text, "applicant record")
    fields = text.split(":")
    if len(fields) != 2:
        raise ValueError("applicant record must contain exactly one ':'")

    category, raw_marks = (field.strip() for field in fields)
    if not category:
        raise ValueError("category cannot be empty")
    if not raw_marks:
        raise ValueError("marks cannot be empty")

    try:
        marks = float(raw_marks)
    except (ValueError, OverflowError) as error:
        raise ValueError("marks must be a valid number") from error
    if not math.isfinite(marks):
        raise ValueError("marks must be finite")
    if marks < 0:
        raise ValueError("marks cannot be negative")

    return category.title(), marks


def marks_average(marks_csv):
    """Return the floor average of a nonempty CSV list of nonnegative integers."""
    _require_text(marks_csv, "marks list")
    fields = marks_csv.split(",")
    if any(not field.strip() for field in fields):
        raise ValueError("marks list cannot contain empty values")

    try:
        values = [int(field.strip()) for field in fields]
    except (ValueError, OverflowError) as error:
        raise ValueError("each mark must be an integer") from error
    if any(value < 0 for value in values):
        raise ValueError("marks cannot be negative")

    return sum(values) // len(values)


def payable_award(text):
    """Apply the existing 18% uplift and deduction, clamping at zero."""
    _require_text(text, "award record")
    fields = text.split("|")
    if len(fields) != 2:
        raise ValueError("award record must contain exactly one '|'")

    raw_award, raw_deduction = (field.strip() for field in fields)
    if not raw_award or not raw_deduction:
        raise ValueError("award and deduction are required")

    try:
        award = float(raw_award)
        deduction = float(raw_deduction)
    except (ValueError, OverflowError) as error:
        raise ValueError("award and deduction must be valid numbers") from error
    if not math.isfinite(award) or not math.isfinite(deduction):
        raise ValueError("award and deduction must be finite")
    if award < 0 or deduction < 0:
        raise ValueError("award and deduction cannot be negative")

    total = award * 1.18 - deduction
    if not math.isfinite(total):
        raise ValueError("calculated award is outside the supported numeric range")
    return max(total, 0.0)


def _run_section(title, prompt, operation, result_label):
    print(f"==== Running {title} ====")
    try:
        user_input = input(prompt)
        result = operation(user_input)
    except ValueError as error:
        print(f"Invalid input: {error}")
    else:
        print(f"{result_label}: {result}")


def main():
    """Run all three interactive examples and continue after invalid input."""
    _run_section(
        "parse_applicant",
        "Enter category:marks (e.g. merit:82): ",
        parse_applicant,
        "Category and Marks",
    )
    print()
    _run_section(
        "marks_average",
        "Enter marks as CSV (e.g. 72,85,90): ",
        marks_average,
        "Average Marks",
    )
    print()
    _run_section(
        "payable_award",
        "Enter award|deduction (e.g. 5000|500): ",
        payable_award,
        "Payable Award",
    )


if __name__ == "__main__":
    main()
