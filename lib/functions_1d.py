import math

import numpy as np
from noise import pnoise1
from scipy.interpolate import interp1d

from lib.function_modifiers import add, repeat, shift, multiply


def constant(c):
    return lambda v: np.full_like(np.array(v), c, dtype=float)


def linear_interpolation(target_low, target_high, source_low=0, source_high=1):
    if np.allclose(target_low, target_high) or source_low == source_high:
        return lambda v: target_low

    def f(v):
        source_range = source_high - source_low
        over_low = v - source_low
        ratio = over_low / source_range
        return target_low + (target_high - target_low) * ratio

    return f


def square():
    return lambda v: v * v


def sinus():
    return lambda v: np.sin(v * np.pi * 2)


def cosinus():
    return lambda v: np.cos(v * np.pi * 2)


def noise(octaves=4):
    def f(v):
        try:
            result = [pnoise1(t, octaves=octaves) for t in v]
        except TypeError:
            return pnoise1(v, octaves=octaves)
        return result

    return f


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


def stairs(steps, ascend_ratio):
    ascend_ratio /= steps
    vx = []
    x_step_size = 1 / steps
    for i in range(steps + 1):
        vx.append(i * x_step_size - ascend_ratio)
        vx.append(i * x_step_size + ascend_ratio)

    vx = vx[1:-1]
    vx[0] = 0
    vx[-1] = 1

    vy = []
    y_step_size = 1 / (steps - 1)
    for i in range(steps):
        step_y = (i * y_step_size)
        vy.append(step_y)
        vy.append(step_y)

    return interp1d(vx, vy, kind='linear')


def arc():
    f = add(square(), constant(-1))
    f = repeat(2, f, 'zigzag')
    f = shift(0.5, f)
    f = multiply(f, constant(-1))
    return f
