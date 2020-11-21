import numpy as np

from stitch_generator.functions.calculate_direction import calculate_direction
from stitch_generator.functions.functions_1d import linear_interpolation
from stitch_generator.functions.functions_2d import function_2d, circle, line, spiral, bezier, bezier_normals
from stitch_generator.sampling.sample_by_number import sample_by_number


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
    f = line((0, 0), (100, 20))
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


def test_bezier():
    control_points = np.array(((0, 0), (20, 20), (40, -20), (60, 0), (80, 0)))

    functions = [
        bezier(control_points[0:3, :]),
        bezier(control_points[0:4, :]),
        bezier(control_points)
    ]

    for f in functions:
        samples = f(sample_by_number(10, include_endpoint=True))
        # no specific check for coordinates, just check that we get a ndarray
        assert isinstance(samples, np.ndarray)
        assert len(samples) == 11


def test_bezier_normals():
    control_points = ((0, 0), (10, 0), (20, 0))

    f = bezier(control_points)
    direction = bezier_normals(control_points)

    samples = sample_by_number(10, include_endpoint=True)
    points = f(samples)
    directions = direction(samples)

    comparison = calculate_direction(points)

    assert np.allclose(directions, comparison)
