import numpy as np
import pytest

from stitch_generator.collection.functions import linear_0_1
from stitch_generator.functions import constant
from stitch_generator.helpers import get_boundaries, path_from_boundaries
from stitch_generator.shapes import bezier_shape, line_shape

boundary_pairs = [
    (line_shape((0, 0), (10, 0)), line_shape((0, 5), (10, 5))),
    (
        bezier_shape(((0, 0), (10, -10), (20, 0))),
        bezier_shape(((0, 3), (10, -4), (20, 6))),
    ),
]


@pytest.mark.parametrize("left, right", boundary_pairs)
@pytest.mark.parametrize(
    "alignment", [constant(0), constant(0.5), constant(1), linear_0_1]
)
def test_path_from_boundaries_round_trip(left, right, alignment):
    path = path_from_boundaries(left, right, alignment)
    new_left, new_right = get_boundaries(path)

    t = np.linspace(0, 1, 11)
    assert np.allclose(new_left(t), left(t))
    assert np.allclose(new_right(t), right(t))
