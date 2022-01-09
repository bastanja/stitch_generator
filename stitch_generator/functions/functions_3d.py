import numpy as np

from stitch_generator.functions.ensure_shape import ensure_1d_shape
from stitch_generator.framework.types import Function3D, Function1D


def function_3d(fx: Function1D, fy: Function1D, fz: Function1D) -> Function3D:
    def f(t):
        t = ensure_1d_shape(t)
        return np.array([fx(t), fy(t), fz(t)]).T

    return f
