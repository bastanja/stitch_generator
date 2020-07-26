from functools import partial

import numpy as np
from noise import pnoise1
from scipy.interpolate import interp1d


def function_1d(f):
    def wrapper(v):
        v = np.asarray(v)
        try:
            result = np.asarray(f(v)).reshape(v.shape)
        except TypeError:
            result = np.array([f(t) for t in v.squeeze()]).reshape(v.shape)
        return result

    return wrapper


def constant(c):
    return lambda v: np.full_like(np.array(v), c, dtype=float)


def linear_interpolation(target_low, target_high, source_low=0, source_high=1):
    if source_low == source_high:
        return constant(target_low)
    return interp1d([source_low, source_high], [target_low, target_high], fill_value="extrapolate")


def square():
    return lambda v: np.asarray(np.asarray(v) * np.asarray(v))


def sinus():
    return lambda v: np.asarray(np.sin(np.asarray(v) * np.pi * 2))


def cosinus():
    return lambda v: np.asarray(np.cos(np.asarray(v) * np.pi * 2))


def noise(octaves=4):
    n = partial(pnoise1, octaves=octaves)
    return function_1d(n)


def cubic_interpolation_evenly_spaced(values):
    assert len(values) > 1, "Interpolation function needs at least two values"
    samples = np.linspace(0, 1, num=len(values), endpoint=True)

    # Use cubic interpolation (3) if there are enough samples,
    # otherwise reduce to len(samples) - 1, i.e. quadratic (2) or linear (1)
    interpolation = min(len(samples) - 1, 3)

    f = interp1d(samples, values, kind=interpolation)
    return f


def arc():
    return lambda v: np.asarray(1 - ((np.asarray(v) * 2) - 1) ** 2)


def smoothstep():
    return lambda v: np.asarray(3 * np.asarray(v) ** 2 - 2 * np.asarray(v) ** 3)


def smootherstep():
    return lambda v: np.asarray(6 * np.asarray(v) ** 5 - 15 * np.asarray(v) ** 4 + 10 * np.asarray(v) ** 3)


def circular_arc():
    return lambda v: np.asarray(np.sqrt(1 - (1 - np.asarray(v)) ** 2))
