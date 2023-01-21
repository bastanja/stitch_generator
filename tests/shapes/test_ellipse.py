import numpy as np
import pytest

from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number
from stitch_generator.shapes.ellipse import ellipse
from tests.shapes.normal_length import normal_length_one


@pytest.mark.parametrize("center, rx, ry", [
    ((0, 0), 5, 2.2),
    ((10, 10), 5, 10),  # center not zero
    ((10, 10), 0, 10),  # radius x zero
])
def test_ellipse(center, rx, ry):
    shape, direction = ellipse(center=center, rx=rx, ry=ry)

    # check that directions are normalized
    assert normal_length_one(direction)

    # check that ellipse is closed
    assert np.allclose(shape(0), shape(1))
