import numpy as np
import pytest

from stitch_generator.shapes.rounded_rect import simple_rounded_rect, rounded_rect_with_corner_radii
from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number
from tests.shapes.normal_length import normal_length_one


def position_not_zero(shape) -> bool:
    positions = shape(subdivide_by_number(1000))
    non_zero = positions != (0, 0)
    return np.alltrue(non_zero)


@pytest.mark.parametrize("width, height, corner_radius", [
    (5, 5, 1),
    (5, 0, 1),
    (2.2, 4.4, 0),
    (5, 5, 10)
])
def test_simple_rounded_rect(width, height, corner_radius):
    radii = [(corner_radius, corner_radius) for _ in range(4)]
    shape, direction = simple_rounded_rect(width=width, height=height, corner_radius=corner_radius)

    # check that directions are normalized
    assert normal_length_one(direction)

    # check that position is not (0,0)
    if width != 0 and height != 0:
        assert position_not_zero(shape)


@pytest.mark.parametrize("width, height, corner_radii", [
    (5, 5, (1, 0, 1, 0))
])
def test_rounded_rect_with_corner_radii(width, height, corner_radii):
    shape, direction = rounded_rect_with_corner_radii(width=width, height=height, corner_radii=corner_radii)

    # check that directions are normalized
    assert normal_length_one(direction)

    # check that position is not (0,0)
    if width != 0 and height != 0:
        assert position_not_zero(shape)
