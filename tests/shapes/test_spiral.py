import numpy as np
import pytest

from stitch_generator.shapes.spiral import spiral, spiral_shape
from tests.shapes.normal_length import normal_length_one


@pytest.mark.parametrize("inner_radius, outer_radius, turns, center", [
    (0, 1.5, 5, (0, 0)),
    (2.2, 10, 0.5, (0, 0)),
    (1, 2, 3, (4, 5)),
    (10, 2, 5, (10, 10)),
    (1, 2, 0, (0, 0)),
])
def test_spiral(inner_radius, outer_radius, turns, center):
    shape, direction = spiral(inner_radius, outer_radius, turns, center)

    # check that directions are normalized
    assert normal_length_one(direction)

    # check radius at start and end
    assert np.linalg.norm(shape(0) - center) == inner_radius
    assert np.linalg.norm(shape(1) - center) == outer_radius


def test_spiral_shape():
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
