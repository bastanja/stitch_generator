from typing import Sequence

import math
import numpy as np
from scipy.interpolate import interp1d

from stitch_generator.functions.de_casteljau import de_casteljau
from stitch_generator.functions.ensure_shape import ensure_1d_shape, ensure_2d_shape
from stitch_generator.functions.function_modifiers import scale, add, repeat, mix
from stitch_generator.functions.functions_1d import cosinus, sinus, constant, linear_interpolation
from stitch_generator.stitch_operations.rotate import rotate_by_degrees
from stitch_generator.utilities.types import Function2D, Function1D


def function_2d(fx: Function1D, fy: Function1D) -> Function2D:
    def f(t):
        t = ensure_1d_shape(t)
        return np.array([fx(t), fy(t)]).T

    return f


def circle(radius: float = 1, center: Sequence[float] = (0, 0)) -> Function2D:
    return ellipse(rx=radius, ry=radius, center=center)


def ellipse(rx: float, ry: float, center: Sequence[float] = (0, 0)) -> Function2D:
    fx = cosinus()
    fy = sinus()
    fx = scale(rx, fx)
    fy = scale(ry, fy)
    f = function_2d(fx, fy)
    if center != (0, 0):
        c = function_2d(constant(center[0]), constant(center[1]))
        f = add(f, c)
    return f


def line(origin: Sequence[float] = (0, 0), to: Sequence[float] = (100, 0)) -> Function2D:
    interpolation_values = np.vstack((origin, to))
    def f(v):
        result = interp1d(np.array([0, 1]), interpolation_values, fill_value="extrapolate", axis=0)(v)
        return ensure_2d_shape(result)
    return f


def spiral(inner_radius: float, outer_radius: float, turns: float, center: Sequence[float] = (0, 0)) -> Function2D:
    inner_circle = repeat(turns, circle(inner_radius, center=center))
    outer_circle = repeat(turns, circle(outer_radius, center=center))
    return mix(inner_circle, outer_circle, linear_interpolation(0, 1))


def bezier(control_points: Sequence) -> Function2D:
    control_points = np.asarray(control_points, dtype=float)

    def f(v):
        points, tangents = de_casteljau(control_points, np.array(v, ndmin=1, dtype=float))
        return points

    return f


def bezier_normals(control_points: Sequence) -> Function2D:
    control_points = np.asarray(control_points, dtype=float)

    def f(v):
        points, tangents = de_casteljau(control_points, np.array(v, ndmin=1, dtype=float))
        return rotate_by_degrees(tangents, -90)

    return f


def constant_direction(x: float, y: float, normalized: bool = False) -> Function2D:
    if normalized:
        length = math.sqrt(x * x + y * y)
        x /= length
        y /= length
    return function_2d(constant(x), constant(y))
