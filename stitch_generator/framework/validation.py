"""Validation utility functions for common parameter checks.

This module provides reusable validation functions to reduce code duplication
and ensure consistent error handling across the codebase.
"""

from typing import Union

import numpy as np

from stitch_generator.framework.exceptions import (
    InsufficientDataError,
    InvalidParameterError,
)

# Constants for validation thresholds
DUPLICATE_THRESHOLD = 1e-10  # Threshold for considering values as duplicates


def validate_finite(value: Union[float, int], param_name: str = "parameter") -> None:
    """Validates that a value is finite (not NaN or Inf).

    Args:
        value: The value to validate.
        param_name: Name of the parameter for error messages.

    Raises:
        InvalidParameterError: If the value is NaN or Inf.

    Example:
        >>> validate_finite(5.0, "repeat_count")
        >>> validate_finite(np.inf, "repeat_count")  # Raises InvalidParameterError
    """
    if np.isnan(value) or np.isinf(value):
        raise InvalidParameterError(
            f"{param_name} must be a finite number, got {value}"
        )


def validate_finite_array(
    values: Union[list, np.ndarray], param_name: str = "parameter"
) -> None:
    """Validates that all values in an array are finite (not NaN or Inf).

    Args:
        values: The array to validate.
        param_name: Name of the parameter for error messages.

    Raises:
        InvalidParameterError: If any value is NaN or Inf.

    Example:
        >>> validate_finite_array([1.0, 2.0, 3.0], "offsets")
        >>> validate_finite_array([1.0, np.nan], "offsets")  # Raises InvalidParameterError
    """
    values_array = np.asarray(values)
    if np.any(np.isnan(values_array)) or np.any(np.isinf(values_array)):
        raise InvalidParameterError(
            f"{param_name} cannot contain NaN or Inf values"
        )


def validate_range(
    value: float,
    min_val: float,
    max_val: float,
    param_name: str = "parameter",
    inclusive: bool = True,
) -> None:
    """Validates that a value is within a specified range.

    Args:
        value: The value to validate.
        min_val: Minimum allowed value.
        max_val: Maximum allowed value.
        param_name: Name of the parameter for error messages.
        inclusive: If True, values equal to min_val or max_val are valid.

    Raises:
        InvalidParameterError: If the value is outside the range.

    Example:
        >>> validate_range(0.5, 0.0, 1.0, "alignment")
        >>> validate_range(1.5, 0.0, 1.0, "alignment")  # Raises InvalidParameterError
    """
    if inclusive:
        if not (min_val <= value <= max_val):
            raise InvalidParameterError(
                f"{param_name} must be in range [{min_val}, {max_val}], got {value}"
            )
    else:
        if not (min_val < value < max_val):
            raise InvalidParameterError(
                f"{param_name} must be in range ({min_val}, {max_val}), got {value}"
            )


def validate_range_array(
    values: Union[list, np.ndarray],
    min_val: float,
    max_val: float,
    param_name: str = "parameter",
    inclusive: bool = True,
) -> None:
    """Validates that all values in an array are within a specified range.

    Args:
        values: The array to validate.
        min_val: Minimum allowed value.
        max_val: Maximum allowed value.
        param_name: Name of the parameter for error messages.
        inclusive: If True, values equal to min_val or max_val are valid.

    Raises:
        InvalidParameterError: If any value is outside the range.

    Example:
        >>> validate_range_array([0.0, 0.5, 1.0], 0.0, 1.0, "offsets")
        >>> validate_range_array([0.0, 1.5], 0.0, 1.0, "offsets")  # Raises InvalidParameterError
    """
    values_array = np.asarray(values)
    if inclusive:
        invalid_mask = (values_array < min_val) | (values_array > max_val)
    else:
        invalid_mask = (values_array <= min_val) | (values_array >= max_val)

    if np.any(invalid_mask):
        invalid_values = values_array[invalid_mask]
        raise InvalidParameterError(
            f"All {param_name} values must be in range [{min_val}, {max_val}], "
            f"got invalid values: {invalid_values}"
        )


def validate_non_negative(
    value: float, param_name: str = "parameter", allow_zero: bool = True
) -> None:
    """Validates that a value is non-negative.

    Args:
        value: The value to validate.
        param_name: Name of the parameter for error messages.
        allow_zero: If True, zero is allowed.

    Raises:
        InvalidParameterError: If the value is negative (or zero if allow_zero=False).

    Example:
        >>> validate_non_negative(5.0, "width")
        >>> validate_non_negative(-1.0, "width")  # Raises InvalidParameterError
    """
    if allow_zero:
        if value < 0:
            raise InvalidParameterError(
                f"{param_name} must be non-negative, got {value}"
            )
    else:
        if value <= 0:
            raise InvalidParameterError(
                f"{param_name} must be positive, got {value}"
            )


def validate_array_length(
    array: Union[list, np.ndarray],
    min_length: int,
    param_name: str = "array",
    exact_length: Union[int, None] = None,
) -> None:
    """Validates that an array has the required length.

    Args:
        array: The array to validate.
        min_length: Minimum required length.
        param_name: Name of the parameter for error messages.
        exact_length: If provided, the array must have exactly this length.

    Raises:
        InsufficientDataError: If the array doesn't meet length requirements.

    Example:
        >>> validate_array_length([1, 2, 3], 2, "control_points")
        >>> validate_array_length([1], 2, "control_points")  # Raises InsufficientDataError
        >>> validate_array_length([1, 2], 2, "control_points", exact_length=2)
    """
    length = len(array)
    if exact_length is not None:
        if length != exact_length:
            raise InsufficientDataError(
                f"{param_name} must have exactly {exact_length} elements, got {length}"
            )
    else:
        if length < min_length:
            raise InsufficientDataError(
                f"{param_name} must have at least {min_length} elements, got {length}"
            )


def validate_no_duplicates(
    values: Union[list, np.ndarray],
    param_name: str = "parameter",
    threshold: float = DUPLICATE_THRESHOLD,
) -> None:
    """Validates that an array contains no duplicate values.

    Args:
        values: The array to validate.
        param_name: Name of the parameter for error messages.
        threshold: Minimum difference between values to be considered distinct.

    Raises:
        InvalidParameterError: If duplicates are found.

    Example:
        >>> validate_no_duplicates([0.0, 0.5, 1.0], "offsets")
        >>> validate_no_duplicates([0.0, 0.0, 1.0], "offsets")  # Raises InvalidParameterError
    """
    if len(values) <= 1:
        return  # No duplicates possible

    values_array = np.asarray(values)
    diffs = np.diff(np.sort(values_array))
    if np.any(np.abs(diffs) < threshold):
        raise InvalidParameterError(
            f"{param_name} must contain unique values (no duplicates within {threshold})"
        )


def validate_sorted(
    values: Union[list, np.ndarray],
    param_name: str = "parameter",
    strict: bool = False,
) -> None:
    """Validates that an array is sorted.

    Args:
        values: The array to validate.
        param_name: Name of the parameter for error messages.
        strict: If True, values must be strictly increasing (no duplicates).

    Raises:
        InvalidParameterError: If the array is not sorted.

    Example:
        >>> validate_sorted([0.0, 0.5, 1.0], "offsets")
        >>> validate_sorted([0.5, 0.0, 1.0], "offsets")  # Raises InvalidParameterError
    """
    values_array = np.asarray(values)
    if strict:
        if np.any(values_array[1:] <= values_array[:-1]):
            raise InvalidParameterError(
                f"{param_name} must be strictly increasing (sorted with no duplicates)"
            )
    else:
        if np.any(values_array[1:] < values_array[:-1]):
            raise InvalidParameterError(
                f"{param_name} must be sorted in ascending order"
            )


def validate_unit_range(
    value: float, param_name: str = "parameter"
) -> None:
    """Validates that a value is in the unit range [0, 1].

    Convenience function for validate_range(value, 0.0, 1.0, param_name).

    Args:
        value: The value to validate.
        param_name: Name of the parameter for error messages.

    Raises:
        InvalidParameterError: If the value is outside [0, 1].

    Example:
        >>> validate_unit_range(0.5, "alignment")
        >>> validate_unit_range(1.5, "alignment")  # Raises InvalidParameterError
    """
    validate_range(value, 0.0, 1.0, param_name)


def validate_unit_range_array(
    values: Union[list, np.ndarray], param_name: str = "parameter"
) -> None:
    """Validates that all values in an array are in the unit range [0, 1].

    Convenience function for validate_range_array(values, 0.0, 1.0, param_name).

    Args:
        values: The array to validate.
        param_name: Name of the parameter for error messages.

    Raises:
        InvalidParameterError: If any value is outside [0, 1].

    Example:
        >>> validate_unit_range_array([0.0, 0.5, 1.0], "offsets")
        >>> validate_unit_range_array([0.0, 1.5], "offsets")  # Raises InvalidParameterError
    """
    validate_range_array(values, 0.0, 1.0, param_name)
