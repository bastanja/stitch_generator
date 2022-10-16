from typing import Sequence, Tuple

import numpy as np
from scipy.interpolate import interp1d

from stitch_generator.framework.types import Function2D
from stitch_generator.functions.ensure_shape import ensure_2d_shape
from stitch_generator.functions.functions_2d import constant_direction
from stitch_generator.stitch_operations.rotate import rotate_270


def line(origin: Sequence[float] = (0, 0), to: Sequence[float] = (100, 0)) -> Tuple[Function2D, Function2D]:
    shape = line_shape(origin=origin, to=to)
    direction = line_direction(origin=origin, to=to)
    return shape, direction


def line_shape(origin: Sequence[float] = (0, 0), to: Sequence[float] = (100, 0)) -> Function2D:
    interpolation = interp1d(np.array([0, 1]), np.vstack((origin, to)), fill_value="extrapolate", axis=0)

    def f(v):
        result = interpolation(v)
        return ensure_2d_shape(result)

    return f


def line_direction(origin: Sequence[float] = (0, 0), to: Sequence[float] = (100, 0)) -> Function2D:
    delta = ensure_2d_shape(np.asarray(to) - np.asarray(origin))
    length = np.linalg.norm(delta)
    delta = (delta / length) if length > 0 else delta
    direction = rotate_270(delta)
    return constant_direction(direction[0][0], direction[0][1])
