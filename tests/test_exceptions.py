import pytest

from app.exceptions import (
    CalculatorError,
    ValidationError,
    OperationError,
    ConfigurationError,
)


@pytest.mark.parametrize(
    "exception_class",
    [
        ValidationError,
        OperationError,
        ConfigurationError,
    ],
)
def test_exception_inheritance(exception_class):
    assert issubclass(exception_class, CalculatorError)


def test_calculator_error_message():
    with pytest.raises(CalculatorError, match="Test error"):
        raise ValidationError("Test error")