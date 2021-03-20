from typing import Sequence

import numpy as np
from scipy.interpolate import interp1d

from stitch_generator.functions.ensure_shape import ensure_2d_shape
from stitch_generator.utilities.types import Function2D


def line(origin: Sequence[float] = (0, 0), to: Sequence[float] = (100, 0)) -> Function2D:
    interpolation_values = np.vstack((origin, to))

    def f(v):
        result = interp1d(np.array([0, 1]), interpolation_values, fill_value="extrapolate", axis=0)(v)
        return ensure_2d_shape(result)

    return f
