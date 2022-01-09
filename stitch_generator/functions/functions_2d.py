import math
import numpy as np

from stitch_generator.functions.ensure_shape import ensure_1d_shape
from stitch_generator.functions.functions_1d import constant
from stitch_generator.framework.types import Function2D, Function1D


def function_2d(fx: Function1D, fy: Function1D) -> Function2D:
    def f(t):
        t = ensure_1d_shape(t)
        return np.array([fx(t), fy(t)]).T

    return f


def constant_direction(x: float, y: float, normalized: bool = False) -> Function2D:
    if normalized:
        length = math.sqrt(x * x + y * y)
        x /= length
        y /= length
    return function_2d(constant(x), constant(y))
