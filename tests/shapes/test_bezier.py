import numpy as np
import pytest

from stitch_generator.shapes.bezier import bezier
from tests.shapes.normal_length import normal_length_one


@pytest.mark.parametrize("points", [
    ((0, 0), (10, 0), (20, 0), (30, 0)),
    ((0, 0), (10, 0), (10, 0), (20, 0)),
    ((0, 0), (10, 0), (20, 0)),
    ((5.5, 0), (10, 50), (5.5, 10)),
    ((0, 0), (10, 10), (20, 0), (30, 10), (40, 0), (50, 10), (60, 0)),
])
def test_bezier(points):
    shape, direction = bezier(points)

    # check that directions are normalized
    assert normal_length_one(direction)

    # check start and end point
    assert np.allclose(shape(0), points[0])
    assert np.allclose(shape(1), points[-1])
