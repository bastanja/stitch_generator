import math

import numpy as np
from noise import pnoise1
from scipy.interpolate import interp1d


def constant(v):
    return lambda _: v


def linear_interpolation(target_low, target_high, source_low=0, source_high=1):
    def f(v):
        if target_low == target_high or source_high == source_low:
            return target_low
        source_range = source_high - source_low
        over_low = v - source_low
        ratio = over_low / source_range
        return target_low + (target_high - target_low) * ratio

    return f


def square():
    return lambda v: v * v


def sinus():
    return lambda v: math.sin(v * math.pi * 2)


def cosinus():
    return lambda v: math.cos(v * math.pi * 2)


def noise():
    return lambda v: pnoise1(v, octaves=4)


def positive_noise():
    return lambda v: (noise()(v) + 1) * 0.5


def cubic_interpolation_evenly_spaced(values):
    assert len(values) > 1, "Interpolation function needs at least two values"
    samples = np.linspace(0, 1, num=len(values), endpoint=True)

    # Use cubic interpolation (3) if there are enough samples,
    # otherwise reduce to len(samples) - 1, i.e. quadratic (2) or linear (1)
    interpolation = min(len(samples) - 1, 3)

    f = interp1d(samples, values, kind=interpolation)
    return f

