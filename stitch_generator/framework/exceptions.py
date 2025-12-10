"""Custom exception classes for stitch_generator."""


class StitchGeneratorError(Exception):
    """Base exception for all stitch_generator errors."""
    pass


class InvalidPathError(StitchGeneratorError):
    """Raised when a path is invalid or cannot be processed."""
    pass


class InvalidParameterError(StitchGeneratorError):
    """Raised when a parameter is out of valid range or has an invalid value."""
    pass


class InsufficientDataError(StitchGeneratorError):
    """Raised when there is insufficient data to perform an operation."""
    pass


class InvalidInputError(StitchGeneratorError):
    """Raised when input data is invalid or malformed."""
    pass
