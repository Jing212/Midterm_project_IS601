"""Define custom calculator exceptions."""

class CalculatorError(Exception):
    """Base exception for the calculator application."""



class ValidationError(CalculatorError):
    """Raised when user input is invalid."""



class OperationError(CalculatorError):
    """Raised when a calculation cannot be performed."""



class ConfigurationError(CalculatorError):
    """Raised when calculator configuration is invalid."""
