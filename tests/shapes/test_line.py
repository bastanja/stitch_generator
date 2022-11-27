import numpy as np
import pytest

from stitch_generator.shapes.line import line
from tests.shapes.normal_length import normal_length_one


@pytest.mark.parametrize("origin, to", [
    ((0, 0), (100, 0)),
    ((10, 10), (55.5, 0)),
    ((-10, -10), (0, 0))
])
def test_line(origin, to):
    shape, direction = line(origin=origin, to=to)

    # check that directions are normalized
    assert normal_length_one(direction)

    # check start and end point
    assert np.allclose(shape(0), origin)
    assert np.allclose(shape(1), to)
