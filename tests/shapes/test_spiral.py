import numpy as np
import pytest

from stitch_generator.shapes.spiral import spiral
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
