from typing import Literal, Callable, Union, List

import numpy as np

from stitch_generator.framework import InvalidParameterError
from stitch_generator.framework import Function2D, Function1D, Array1D
from stitch_generator.framework import (
    DUPLICATE_THRESHOLD,
    validate_finite,
    validate_finite_array,
    validate_no_duplicates,
    validate_unit_range_array,
)
from .ensure_shape import ensure_1d_shape


def reflect(function):
    """Reflects a function at its boundaries, creating a mirror effect.

    The function is repeated with reflection at x=0 and x=1, creating a pattern
    that mirrors back and forth. For values outside [0, 1], the function is
    reflected: f(-0.3) = f(0.3), f(1.3) = f(0.7), etc.

    Args:
        function: A function to reflect. Should be defined in the range [0, 1].

    Returns:
        A new function of the same type that applies reflection to the input before calling
        the original function.

    Example:
        >>> f = reflect(lambda v: v)
        >>> f(0.3)  # Returns 0.3
        >>> f(1.3)  # Returns 0.7 (reflected)
    """

    def f(v):
        val = 1 - (np.absolute(1 - (v % 2)))
        return function(val)

    return f


def wrap(function):
    """Wraps a function by applying modulo 1 to the input.

    Values outside [0, 1] are wrapped back into the range using modulo
    arithmetic. This creates a repeating pattern.

    Args:
        function: A function to wrap. Should be defined in the range [0, 1].

    Returns:
        A new function of the same type that wraps the input to [0, 1] before calling
        the original function.

    Example:
        >>> f = wrap(lambda v: v)
        >>> f(0.3)  # Returns 0.3
        >>> f(1.3)  # Returns 0.3 (wrapped)
        >>> f(2.7)  # Returns 0.7 (wrapped)
    """
    return lambda v: function(v % 1)


def clamp(function):
    """Clamps input values to [0, 1] before applying the function.

    Values less than 0 are clamped to 0, and values greater than 1 are
    clamped to 1. This prevents the function from being evaluated outside
    its defined range.

    Args:
        function: A function to clamp. Should be defined in the range [0, 1].

    Returns:
        A new function of the same type that clamps the input to [0, 1] before calling
        the original function.

    Example:
        >>> f = clamp(lambda v: v)
        >>> f(0.3)   # Returns 0.3
        >>> f(-0.5)  # Returns 0.0 (clamped)
        >>> f(1.5)   # Returns 1.0 (clamped)
    """

    def f(v):
        v = np.asarray(v)
        v[v < 0] = 0.0
        v[v > 1] = 1.0
        return function(v)

    return f


def repeat(r: float, function, mode: Literal["", "reflect", "wrap", "clamp"] = ""):
    """Repeats a function multiple times by scaling the input domain.

    The function is repeated `r` times across the input range [0, 1]. For example,
    if r=2, the function will be evaluated twice: once for inputs [0, 0.5] and
    once for inputs [0.5, 1].

    Args:
        r: The number of times to repeat the function.
        function: A function to repeat. Should be defined in the range [0, 1].
        mode: How to handle values outside [0, 1] when repeating:
            - '' (empty): No special handling
            - 'reflect': Use reflection at boundaries (see `reflect()`)
            - 'wrap': Wrap values using modulo (see `wrap()`)
            - 'clamp': Clamp values to [0, 1] (see `clamp()`)

    Returns:
        A new function of the same type that repeats the original function `r` times.

    Raises:
        InvalidParameterError: If r is NaN/Inf.

    Example:
        >>> f = repeat(2, lambda v: v)
        >>> f(0.25)  # Evaluates original function at 0.5
        >>> f(0.75)  # Evaluates original function at 1.5 (wrapped to 0.5)
    """

    validate_finite(r, "Repeat count r")

    if mode == "reflect":
        function = reflect(function)
    if mode == "wrap":
        function = wrap(function)
    if mode == "nearest":
        function = clamp(function)
    return lambda v: function(np.asarray(v) * r)


def scale(s: float, function):
    """Scales the output of a function by a constant factor.

    Multiplies all output values of the function by the scale factor `s`.
    This is useful for adjusting the magnitude of function values without
    changing their shape.

    Args:
        s: The scale factor to multiply function outputs by.
        function: A function to scale.

    Returns:
        A new function of the same type that returns scaled values.

    Example:
        >>> f = scale(2.0, lambda v: v)
        >>> f(0.5)  # Returns 1.0 (0.5 * 2.0)
    """
    return lambda v: function(v) * s


def shift(amount: float, function):
    """Shifts a function's input domain by a constant amount.

    Translates the input parameter by `amount` before evaluating the function.
    This effectively shifts the function along its domain.

    Args:
        amount: The amount to shift the input parameter. Can be positive or negative.
        function: A function to shift.

    Returns:
        A new function of the same type that evaluates the original function
        at shifted parameter values.

    Example:
        >>> f = shift(0.2, lambda v: v)
        >>> f(0.3)  # Evaluates original function at 0.5 (0.3 + 0.2)
        >>> f(0.0)  # Evaluates original function at 0.2
    """
    return lambda v: function(v + amount)


def compose(f1, f2):
    """Composes two functions by composing them together.

    Creates a new function that first applies `f1` to the input, then applies
    `f2` to the result. This is function composition: compose(f1, f2)(x) = f2(f1(x)).

    Args:
        f1: The first function to apply. Can be 1D, 2D, or 3D.
        f2: The second function to apply. Must accept the output type of `f1`.

    Returns:
        A new function that applies `f1` followed by `f2`. The return type
        matches the return type of `f2`.

    Example:
        >>> f1 = lambda v: v * 2
        >>> f2 = lambda v: v + 1
        >>> composed = compose(f1, f2)
        >>> composed(3)  # Returns 7 (f2(f1(3)) = f2(6) = 7)
    """
    return lambda v: f2(f1(v))


def add_functions(f1, f2):
    """Adds two functions element-wise.

    Creates a new function that returns the sum of outputs from `f1` and `f2`
    when evaluated at the same input. Both functions must return arrays of
    compatible shapes.

    Args:
        f1: A function to add.
        f2: A function to add. Must return arrays of the same shape
            as `f1` for the same input.

    Returns:
        A new function of the same type that returns f1(v) + f2(v).

    Example:
        >>> f1 = lambda v: v
        >>> f2 = lambda v: v * 2
        >>> added = add_functions(f1, f2)
        >>> added(0.5)  # Returns 1.5 (0.5 + 1.0)
    """
    return _binary_operation(lambda a, b: a + b, f1, f2)


def subtract_functions(f1, f2):
    """Subtracts two functions element-wise.

    Creates a new function that returns the difference of outputs from `f1` and `f2`
    when evaluated at the same input: f1(v) - f2(v).

    Args:
        f1: A function (minuend).
        f2: A function (subtrahend). Must return arrays of the same shape
            as `f1` for the same input.

    Returns:
        A new function of the same type that returns f1(v) - f2(v).

    Example:
        >>> f1 = lambda v: v * 2
        >>> f2 = lambda v: v
        >>> subtracted = subtract_functions(f1, f2)
        >>> subtracted(0.5)  # Returns 0.5 (1.0 - 0.5)
    """
    return _binary_operation(lambda a, b: a - b, f1, f2)


def multiply_functions(f1, f2):
    """Multiplies two functions element-wise.

    Creates a new function that returns the product of outputs from `f1` and `f2`
    when evaluated at the same input: f1(v) * f2(v).

    Args:
        f1: A function to multiply.
        f2: A function to multiply. Must return arrays of the same shape
            as `f1` for the same input.

    Returns:
        A new function of the same type that returns f1(v) * f2(v).

    Example:
        >>> f1 = lambda v: v
        >>> f2 = lambda v: v * 2
        >>> multiplied = multiply_functions(f1, f2)
        >>> multiplied(0.5)  # Returns 0.5 (0.5 * 1.0)
    """
    return _binary_operation(lambda a, b: a * b, f1, f2)


def divide_functions(f1, f2):
    """Divides two functions element-wise with safe division.

    Creates a new function that returns the quotient of outputs from `f1` and `f2`
    when evaluated at the same input: f1(v) / f2(v). Division by zero or negative
    values in `f2` results in zero in the output (safe division).

    Args:
        f1: A function (dividend).
        f2: A function (divisor). Must return arrays of the same shape
            as `f1` for the same input.

    Returns:
        A new function of the same type that returns f1(v) / f2(v) where f2(v) > 0,
        and 0 otherwise.

    Example:
        >>> f1 = lambda v: v * 2
        >>> f2 = lambda v: v + 0.1  # Never zero
        >>> divided = divide_functions(f1, f2)
        >>> divided(0.5)  # Returns approximately 1.67 (1.0 / 0.6)
    """

    def f(a, b):
        notnull = b > 0
        b[notnull] = 1 / b[notnull]
        return a * b

    return _binary_operation(f, f1, f2)


def inverse(function):
    """Reverses a function by inverting its input parameter.

    Creates a new function that evaluates the original function at 1 - v instead
    of v. This effectively reverses the function along its domain [0, 1].

    Args:
        function: A function to invert.

    Returns:
        A new function of the same type that returns function(1 - v).

    Example:
        >>> f = lambda v: v
        >>> inverted = inverse(f)
        >>> inverted(0.2)  # Returns 0.8 (evaluates f at 1 - 0.2 = 0.8)
        >>> inverted(0.8)  # Returns 0.2 (evaluates f at 1 - 0.8 = 0.2)
    """
    return lambda v: function(1 - v)


def mix(f1, f2, factor: Function1D):
    """Linearly interpolates between two functions using a factor function.

    Creates a new function that blends the outputs of `f1` and `f2` based on
    the value returned by `factor`. The interpolation formula is:
    result = (1 - factor(v)) * f1(v) + factor(v) * f2(v)

    When factor(v) = 0, the result equals f1(v). When factor(v) = 1, the result
    equals f2(v). For values in between, the result is a linear interpolation.

    Args:
        f1: A function (start of interpolation).
        f2: A function (end of interpolation). Must return arrays of
            the same shape as `f1` for the same input.
        factor: A 1D function returning interpolation factors in [0, 1].
            Values outside [0, 1] are allowed but may produce unexpected results.

    Returns:
        A new function of the same type that returns the interpolated blend
        of f1(v) and f2(v).

    Example:
        >>> f1 = lambda v: v
        >>> f2 = lambda v: v * 2
        >>> factor = lambda v: v  # Interpolate from f1 to f2
        >>> mixed = mix(f1, f2, factor)
        >>> mixed(0.5)  # Returns 0.75 (0.5 * 0.5 + 1.0 * 0.5)
    """
    one_minus_factor = subtract_functions(
        lambda v: np.ones_like(np.array(v), dtype=float), factor
    )
    return add_functions(
        multiply_functions(f1, one_minus_factor), multiply_functions(f2, factor)
    )


def _binary_operation(operation: Callable, f1, f2):
    """Internal helper function for binary operations on functions.

    Applies a binary operation (like addition, subtraction) to the outputs of
    two functions when evaluated at the same input. Handles shape preservation
    and array broadcasting.

    Args:
        operation: A binary function that takes two arrays and returns an array.
        f1: A function.
        f2: A function. Must return arrays compatible with `f1`.

    Returns:
        A new function that applies the operation to f1(v) and f2(v).
    """

    def f(v):
        original_shape = np.asarray(v).shape
        v = ensure_1d_shape(v)
        v1 = f1(v)
        v2 = f2(v)
        result = operation(v1.T, v2.T).T
        try:
            # if possible, return a result that has the same shape as the parameter v
            result.shape = original_shape
        except ValueError:
            pass
        return result

    return f


def max_functions(f1, f2):
    """Returns the element-wise maximum of two functions.

    Creates a new function that returns the maximum value from `f1` and `f2`
    at each point: max(f1(v), f2(v)).

    Args:
        f1: A function.
        f2: A function. Must return arrays of the same shape as `f1`
            for the same input.

    Returns:
        A new function of the same type that returns the element-wise maximum
        of f1(v) and f2(v).

    Example:
        >>> f1 = lambda v: v
        >>> f2 = lambda v: 1 - v
        >>> max_func = max_functions(f1, f2)
        >>> max_func(0.3)  # Returns 0.7 (max(0.3, 0.7))
    """
    return lambda v: np.maximum(f1(v), f2(v))


def min_functions(f1, f2):
    """Returns the element-wise minimum of two functions.

    Creates a new function that returns the minimum value from `f1` and `f2`
    at each point: min(f1(v), f2(v)).

    Args:
        f1: A function.
        f2: A function. Must return arrays of the same shape as `f1`
            for the same input.

    Returns:
        A new function of the same type that returns the element-wise minimum
        of f1(v) and f2(v).

    Example:
        >>> f1 = lambda v: v
        >>> f2 = lambda v: 1 - v
        >>> min_func = min_functions(f1, f2)
        >>> min_func(0.3)  # Returns 0.3 (min(0.3, 0.7))
    """
    return lambda v: np.minimum(f1(v), f2(v))


def split(function, offsets: Union[List[float], Array1D]):
    """Splits a function into multiple segments at specified offsets.

    Divides the function's domain [0, 1] into segments at the given offsets,
    returning a list of functions, each representing one segment. The segments
    are scaled and shifted so they each operate on the full [0, 1] range.

    Args:
        function: A function to split. Should be defined in [0, 1].
        offsets: A list or array of split points in [0, 1]. The offsets should
            be sorted and unique. The function will be split at these points.

    Returns:
        A list of functions, one for each segment. The number of returned
        functions is len(offsets) + 1. Each function operates on [0, 1] and
        represents the corresponding segment of the original function.

    Raises:
        InvalidParameterError: If offsets are not in [0, 1], not sorted, or contain duplicates.

    Example:
        >>> f = lambda v: v
        >>> segments = split(f, [0.25, 0.75])
        >>> len(segments)  # Returns 3
        >>> segments[0](0.5)  # Evaluates f at 0.125 (first quarter)
        >>> segments[1](0.5)  # Evaluates f at 0.5 (middle half)
        >>> segments[2](0.5)  # Evaluates f at 0.875 (last quarter)
    """
    try:
        offsets = offsets.tolist()  # convert np.ndarray to list
    except AttributeError:
        offsets = list(offsets)  # make sure we have a list

    # Validate offsets
    if len(offsets) > 0:
        # Check for NaN or Inf
        validate_finite_array(offsets, "offsets")

        # Check range [0, 1]
        validate_unit_range_array(offsets, "offsets")

        # Check for duplicates (allowing small floating point differences)
        validate_no_duplicates(offsets, "offsets", DUPLICATE_THRESHOLD)

    combined = [0] + offsets + [1]

    return [
        repeat(o2 - o1, shift(o1, function)) for o1, o2 in zip(combined, combined[1:])
    ]
