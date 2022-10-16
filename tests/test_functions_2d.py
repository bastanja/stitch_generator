import numpy as np

from stitch_generator.functions.functions_1d import linear_interpolation
from stitch_generator.functions.functions_2d import function_2d
from stitch_generator.sampling.sample_by_number import sample_by_number
from stitch_generator.shapes.bezier import bezier, bezier_shape
from stitch_generator.shapes.circle import circle_shape
from stitch_generator.shapes.line import line_shape
from stitch_generator.shapes.spiral import spiral_shape
from stitch_generator.stitch_operations.calculate_direction import calculate_direction


def test_function_2d():
    fx = linear_interpolation(0, 200)
    fy = linear_interpolation(10, 20)
    f = function_2d(fx, fy)

    assert np.allclose(f(0.5), (100, 15))


def test_circle():
    f = circle_shape()
    assert np.allclose(f(0), (1, 0))
    assert np.allclose(f(0.25), (0, 1))
    assert np.allclose(f(0.5), (-1, 0))
    assert np.allclose(f(0.75), (0, -1))
    assert np.allclose(f(1), (1, 0))

    radii = [3, 4, -1, 1]
    centers = [(0, 0), (1, 1), (10, -10), (-5, 0)]
    for radius in radii:
        for center in centers:
            f = circle_shape(radius, center)
            assert np.allclose(f(0), (radius + center[0], 0 + center[1]))
            assert np.allclose(f(0.25), (0 + center[0], radius + center[1]))
            assert np.allclose(f(0.5), (-radius + center[0], 0 + center[1]))
            assert np.allclose(f(0.75), (0 + center[0], -radius + center[1]))
            assert np.allclose(f(1), (radius + center[0], 0 + center[1]))


def test_line():
    f = line_shape((0, 0), (100, 20))
    assert np.allclose(f(0), (0, 0))
    assert np.allclose(f(0.5), (50, 10))
    assert np.allclose(f(1), (100, 20))


def test_spiral():
    # spiral with one turn
    f = spiral_shape(1, 2, 1)
    assert np.allclose(f(0), (1, 0))
    assert np.allclose(f(0.5), (-1.5, 0))
    assert np.allclose(f(1), (2, 0))

    # spiral with four turns
    f = spiral_shape(20, 40, 4)
    assert np.allclose(f(0), (20, 0))
    assert np.allclose(f(0.5), (30, 0))
    assert np.allclose(f(1), (40, 0))

    # spiral with center parameter
    f = spiral_shape(20, 40, 4, (50, 50))
    assert np.allclose(f(0), (20 + 50, 0 + 50))
    assert np.allclose(f(0.5), (30 + 50, 0 + 50))
    assert np.allclose(f(1), (40 + 50, 0 + 50))


def bezier_shape():
    control_points = np.array(((0, 0), (20, 20), (40, -20), (60, 0), (80, 0)))

    functions = [
        bezier_shape(control_points[0:3, :]),
        bezier_shape(control_points[0:4, :]),
        bezier_shape(control_points)
    ]

    for f in functions:
        samples = f(sample_by_number(10))
        # no specific check for coordinates, just check that we get a ndarray
        assert isinstance(samples, np.ndarray)
        assert len(samples) == 11


def test_bezier_direction():
    shape, direction = bezier(((0, 0), (10, 0), (20, 0)))

    samples = sample_by_number(10)

    points = shape(samples)
    directions = direction(samples)

    comparison = calculate_direction(points)
    assert np.allclose(directions, comparison)
