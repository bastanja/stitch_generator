import numpy as np
import pytest
from lib.functions_1d import linear_interpolation
from lib.functions_2d import function_2d, circle, line, spiral, path, cubic_bezier
from lib.sample import sample


def test_function_2d():
    fx = linear_interpolation(0, 200)
    fy = linear_interpolation(10, 20)
    f = function_2d(fx, fy)

    assert np.allclose(f(0.5), (100, 15))


def test_circle():
    f = circle()
    assert np.allclose(f(0), (1, 0))
    assert np.allclose(f(0.25), (0, 1))
    assert np.allclose(f(0.5), (-1, 0))
    assert np.allclose(f(0.75), (0, -1))
    assert np.allclose(f(1), (1, 0))

    radii = [3, 4, -1, 1]
    centers = [(0, 0), (1, 1), (10, -10), (-5, 0)]
    for radius in radii:
        for center in centers:
            f = circle(radius, center)
            assert np.allclose(f(0), (radius + center[0], 0 + center[1]))
            assert np.allclose(f(0.25), (0 + center[0], radius + center[1]))
            assert np.allclose(f(0.5), (-radius + center[0], 0 + center[1]))
            assert np.allclose(f(0.75), (0 + center[0], -radius + center[1]))
            assert np.allclose(f(1), (radius + center[0], 0 + center[1]))


def test_line():
    f = line(100, 20)
    assert np.allclose(f(0), (0, 0))
    assert np.allclose(f(0.5), (50, 10))
    assert np.allclose(f(1), (100, 20))


def test_spiral():
    # spiral with one turn
    f = spiral(1, 2, 1)
    assert np.allclose(f(0), (1, 0))
    assert np.allclose(f(0.5), (-1.5, 0))
    assert np.allclose(f(1), (2, 0))

    # spiral with four turns
    f = spiral(20, 40, 4)
    assert np.allclose(f(0), (20, 0))
    assert np.allclose(f(0.5), (30, 0))
    assert np.allclose(f(1), (40, 0))

    # spiral with center parameter
    f = spiral(20, 40, 4, (50, 50))
    assert np.allclose(f(0), (20 + 50, 0 + 50))
    assert np.allclose(f(0.5), (30 + 50, 0 + 50))
    assert np.allclose(f(1), (40 + 50, 0 + 50))


def test_path():
    paths = ("M 0,0 L 100, 0",
             "M 0,0 C 20,-20 75,0 75,0",
             "M 0,0 C 5,-15 25,0 25,0 L 40,-15 L 55,0",
             "M 0,0 C 0,-15 40,-5 50,0 C 60,5 75,10 75,0")
    # call the path function with multiple different path strings
    for p in paths:
        path_function = path(p)
        path_points = sample(path_function, 10)
        # no specific check for coordinates, just check that we get a ndarray
        assert isinstance(path_points, np.ndarray)


def test_cubic_bezier():
    p0 = (0,0)
    p1 = (20, 20)
    p2 = (40, -20)
    p3 = (60, 0)
    p4 = (80, 0)

    # check that cubic bezier can't be constructed with three points
    with pytest.raises(Exception):
        bezier = cubic_bezier((p0, p1, p2))

    # check that cubic bezier can't be constructed with five points
    with pytest.raises(Exception):
        bezier = cubic_bezier((p0, p1, p2, p3, p4))

    # check that cubic bezier can be constructed with four points
    bezier = cubic_bezier((p0, p1, p2, p3))
    samples = sample(bezier, 10)
    # no specific check for coordinates, just check that we get a ndarray
    assert isinstance(samples, np.ndarray)
