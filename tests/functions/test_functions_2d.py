import numpy as np

from stitch_generator.functions.functions_1d import linear_interpolation
from stitch_generator.functions.functions_2d import function_2d


def test_function_2d():
    fx = linear_interpolation(0, 200)
    fy = linear_interpolation(10, 20)
    f = function_2d(fx, fy)

    assert np.allclose(f(0.5), (100, 15))
