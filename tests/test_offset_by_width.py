import numpy as np

from stitch_generator.functions.functions_1d import constant, linear_interpolation
from stitch_generator.functions.functions_2d import line, function_2d
from stitch_generator.functions.offset_by_width import offset_by_width, offset_half_width


def test_offset_by_width():
    position = line((0, 0), (100, 0))
    direction = function_2d(constant(0), constant(1))
    width = linear_interpolation(10, 20)

    f = offset_by_width(position, direction, width, False, 1)
    assert np.allclose(f(0), (0, 10))
    assert np.allclose(f(0.5), (50, 15))
    assert np.allclose(f(1), (100, 20))

    f = offset_by_width(position, direction, width, False, 0)
    assert np.allclose(f(0), (0, 0))
    assert np.allclose(f(0.5), (50, 0))
    assert np.allclose(f(1), (100, 0))

    f = offset_by_width(position, direction, width, True, 1)
    assert np.allclose(f(0), (0, -10))
    assert np.allclose(f(0.5), (50, -15))
    assert np.allclose(f(1), (100, -20))


def test_offset_half_width():
    position = line((0, 0), (100, 0))
    direction = function_2d(constant(0), constant(1))
    width = linear_interpolation(10, 20)

    f = offset_half_width(position, direction, width)
    assert np.allclose(f(0), (0, -5))
    assert np.allclose(f(0.5), (50, -7.5))
    assert np.allclose(f(1), (100, -10))
