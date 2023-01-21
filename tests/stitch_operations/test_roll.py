import numpy as np

from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number
from stitch_generator.shapes.circle import circle_shape
from stitch_generator.shapes.line import line_shape
from stitch_generator.stitch_operations.roll import roll


def test_roll():
    # different start and end point
    line_stitches = line_shape(origin=(0, 0), to=(10, 0))(subdivide_by_number(10))
    rolled = roll(line_stitches, amount=3)
    assert np.allclose(line_stitches[0], rolled[3])
    assert not np.allclose(line_stitches[0], rolled[-1])

    # same start and end point
    circle_stitches = circle_shape(radius=10)(subdivide_by_number(12))
    rolled = roll(circle_stitches, amount=5)
    assert np.allclose(circle_stitches[0], rolled[5])
    assert np.allclose(rolled[0], rolled[-1])
