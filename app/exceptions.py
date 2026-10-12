class CalculatorError(Exception):
    """Base exception for the calculator application."""
    pass


class ValidationError(CalculatorError):
    """Raised when user input is invalid."""
    pass


class OperationError(CalculatorError):
    """Raised when a calculation cannot be performed."""
    pass


class ConfigurationError(CalculatorError):
    """Raised when calculator configuration is invalid."""
    pass