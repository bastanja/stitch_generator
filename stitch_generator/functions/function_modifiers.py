import numpy as np

from stitch_generator.functions.ensure_shape import ensure_1d_shape
from stitch_generator.stitch_operations.rotate import rotate_by_degrees, rotate_by_radians
from stitch_generator.utilities.types import Function2D, Function1D


def reflect(function):
    def f(v):
        val = 1 - (np.absolute(1 - (v % 2)))
        return function(val)

    return f


def wrap(function):
    return lambda v: function(v % 1)


def nearest(function):
    def f(v):
        if v < 0: v = 0
        if v > 1: v = 1
        return function(v)

    return f


def repeat(r, function, mode=''):
    if mode == 'reflect':
        function = reflect(function)
    if mode == 'wrap':
        function = wrap(function)
    if mode == 'nearest':
        function = nearest(function)
    return lambda v: function(np.asarray(v) * r)


def scale(s, function):
    return lambda v: function(v) * s


def rotate_degrees(stitch_position_function: Function2D, angle_function: Function1D) -> Function2D:
    """
    Creates a rotated 2D Function

    Args:
        stitch_position_function: A 2D Function returning stitch positions
        angle_function:           A 1D Function returning rotation angles in degrees

    Returns:
        A 2D Function that returns the stitches from `stitch_position_function` rotated by the angles from
        `angle_function`
    """
    def f(t):
        t = ensure_1d_shape(t)
        return rotate_by_degrees(stitch_position_function(t), angle_function(t))

    return f


def rotate_radians(stitch_position_function: Function2D, angle_function: Function1D) -> Function2D:
    """
    Creates a rotated 2D Function

    Args:
        stitch_position_function: A 2D Function returning stitch positions
        angle_function:           A 1D Function returning rotation angles in radians

    Returns:
        A 2D Function that returns the stitches from `stitch_position_function` rotated by the angles from
        `angle_function`
    """
    def f(t):
        t = ensure_1d_shape(t)
        return rotate_by_radians(stitch_position_function(t), angle_function(t))

    return f


def shift(amount, function):
    return lambda v: function(v + amount)


def combine(f1, f2):
    return lambda v: f2(f1(v))


def add(f1, f2):
    return _binary_operation(lambda a, b: a + b, f1, f2)


def subtract(f1, f2):
    return _binary_operation(lambda a, b: a - b, f1, f2)


def multiply(f1, f2):
    return _binary_operation(lambda a, b: a * b, f1, f2)


def inverse(function):
    return lambda v: function(1 - v)


def mix(f1, f2, factor):
    one_minus_factor = subtract(lambda v: np.ones_like(np.array(v), dtype=float), factor)
    return add(multiply(f1, one_minus_factor), multiply(f2, factor))


def _binary_operation(operation, f1, f2):
    def f(v):
        v = ensure_1d_shape(v)
        v1 = f1(v)
        v2 = f2(v)
        result = operation(v1.T, v2.T).T
        return result

    return f


def maximum(f1, f2):
    return lambda v: np.maximum(f1(v), f2(v))


def minimum(f1, f2):
    return lambda v: np.minimum(f1(v), f2(v))


def split(function, offsets):
    try:
        offsets = offsets.tolist()  # convert np.ndarray to list
    except AttributeError:
        offsets = list(offsets)  # make sure we have a list

    combined = [0] + offsets + [1]

    return [repeat(o2 - o1, shift(o1, function)) for o1, o2 in zip(combined, combined[1:])]
