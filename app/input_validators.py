"""Validate calculator numerical inputs."""

from decimal import Decimal, InvalidOperation

from app.exceptions import ValidationError


class InputValidator:
    """Validate and convert calculator inputs."""

    @staticmethod
    def validate_number(value, max_value=Decimal("1000000")) -> Decimal:
        """
        Convert input into Decimal and validate its range.
        """

        if isinstance(value, bool):
            raise ValidationError("Boolean values are not valid numbers.")

        try:
            number = Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            raise ValidationError(
                f"Invalid numerical input: {value}"
            ) from None

        if not number.is_finite():
            raise ValidationError(
                "Input must be a finite number."
            )

        try:
            limit = Decimal(str(max_value))
        except (InvalidOperation, ValueError, TypeError):
            raise ValidationError(
                "Maximum input value must be a valid number."
            ) from None

        if not limit.is_finite() or limit <= 0:
            raise ValidationError(
                "Maximum input value must be positive and finite."
            )

        if abs(number) > limit:
            raise ValidationError(
                f"Input must be between {-limit} and {limit}."
            )

        return number
