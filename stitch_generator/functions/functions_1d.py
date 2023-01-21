from typing import Callable

import numpy as np
from scipy.interpolate import interp1d, PchipInterpolator

from stitch_generator.framework.types import Function1D


def function_1d(f: Callable[..., float]) -> Function1D:
    def wrapper(v):
        v = np.asarray(v)
        try:
            result = np.asarray(f(v)).reshape(v.shape)
        except TypeError:
            result = np.array([f(t) for t in v.squeeze()]).reshape(v.shape)
        return result

    return wrapper


def constant(c: float) -> Function1D:
    return lambda v: np.full_like(np.array(v), c, dtype=float)


def linear_interpolation(target_low, target_high, source_low=0, source_high=1) -> Function1D:
    if source_low == source_high:
        return constant(target_low)
    return interp1d([source_low, source_high], [target_low, target_high], fill_value="extrapolate")


def cubic_interpolation(control_points) -> Function1D:
    control_points = np.asarray(control_points)
    assert len(control_points) > 1, "Interpolation function needs at least two values"

    # Use cubic interpolation (3) if there are enough control points,
    # otherwise reduce to len(control_points) - 1, i.e. quadratic (2) or linear (1)
    interpolation = min(len(control_points) - 1, 3)

    return interp1d(control_points[:, 0], control_points[:, 1], kind=interpolation)


def pchip_interpolation(control_points) -> Function1D:
    """
    Piecewise Cubic Hermite Interpolating Polynomial
    """
    control_points = np.asarray(control_points)
    assert len(control_points) > 1, "Interpolation function needs at least two values"

    return PchipInterpolator(control_points[:, 0], control_points[:, 1])


def square(v):
    return np.asarray(np.asarray(v) * np.asarray(v))


def sinus(v):
    return np.asarray(np.sin(np.asarray(v) * np.pi * 2))


def cosinus(v):
    return np.asarray(np.cos(np.asarray(v) * np.pi * 2))


def arc(v):
    return np.asarray(1 - ((np.asarray(v) * 2) - 1) ** 2)


def smoothstep(v):
    return np.asarray(3 * np.asarray(v) ** 2 - 2 * np.asarray(v) ** 3)


def smootherstep(v):
    return np.asarray(6 * np.asarray(v) ** 5 - 15 * np.asarray(v) ** 4 + 10 * np.asarray(v) ** 3)


def circular_arc(v):
    return np.asarray(np.sqrt(1 - (1 - np.asarray(v)) ** 2))
