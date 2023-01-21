import numpy as np
import pytest

from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number
from stitch_generator.shapes.circle import circle, circle_shape
from tests.shapes.normal_length import normal_length_one


@pytest.mark.parametrize("center, radius", [
    ((0, 0), 5),
    ((10, 10), 5),  # center not zero
    ((10, 10), 0),  # radius zerotest_circle.py
])
def test_circle(center, radius):
    shape, direction = circle(center=center, radius=radius)

    # check that directions are normalized
    assert normal_length_one(direction)

    # check that circle is closed
    assert np.allclose(shape(0), shape(1))

    # check that the distance to the center is equal for each point
    positions = shape(subdivide_by_number(1000))
    distances = positions - center
    lengths = np.linalg.norm(distances, axis=1)
    assert np.allclose(lengths, radius)


def test_circle_shape():
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
