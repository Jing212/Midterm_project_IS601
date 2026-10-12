import pytest
from decimal import Decimal

from app.input_validators import InputValidator
from app.exceptions import ValidationError


@pytest.mark.parametrize(
    "value, expected",
    [
        ("10", Decimal("10")),
        ("-5", Decimal("-5")),
        ("3.14", Decimal("3.14")),
        (100, Decimal("100")),
        (0, Decimal("0")),
    ],
)
def test_valid_numbers(value, expected):
    result = InputValidator.validate_number(value)

    assert result == expected


@pytest.mark.parametrize(
    "value",
    ["abc", None, True, "NaN", "Infinity"],
)
def test_invalid_numbers(value):
    with pytest.raises(ValidationError):
        InputValidator.validate_number(value)


def test_number_exceeds_maximum():
    with pytest.raises(ValidationError):
        InputValidator.validate_number(
            "1001",
            max_value=Decimal("1000")
        )


def test_negative_number_exceeds_limit():
    with pytest.raises(ValidationError):
        InputValidator.validate_number(
            "-1001",
            max_value=Decimal("1000")
        )


def test_custom_maximum():
    result = InputValidator.validate_number(
        "500",
        max_value=Decimal("1000")
    )

    assert result == Decimal("500")


def test_invalid_maximum():
    with pytest.raises(ValidationError):
        InputValidator.validate_number(10, max_value=-1)