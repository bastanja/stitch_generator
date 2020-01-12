from pytest import approx

from lib.functions_1d import linear_interpolation
from lib.functions_2d import function_2d, circle, line


def test_function_2d():
    fx = linear_interpolation(0, 200)
    fy = linear_interpolation(10, 20)
    f = function_2d(fx, fy)

    assert f(0.5) == (100, 15)


def test_circle():
    f = circle()
    assert f(0) == approx((1, 0))
    assert f(0.25) == approx((0, 1))
    assert f(0.5) == approx((-1, 0))
    assert f(0.75) == approx((0, -1))
    assert f(1) == approx((1, 0))

    radii = [3, 4, -1, 1]
    centers = [(0, 0), (1, 1), (10, -10), (-5, 0)]
    for radius in radii:
        for center in centers:
            f = circle(radius, center)
            assert f(0) == approx((radius + center[0], 0 + center[1]))
            assert f(0.25) == approx((0 + center[0], radius + center[1]))
            assert f(0.5) == approx((-radius + center[0], 0 + center[1]))
            assert f(0.75) == approx((0 + center[0], -radius + center[1]))
            assert f(1) == approx((radius + center[0], 0 + center[1]))


def test_line():
    f = line(100, 20)
    assert f(0) == approx((0,0))
    assert f(0.5) == approx((50, 10))
    assert f(1) == approx((100, 20))
