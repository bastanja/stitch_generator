import numpy as np

from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number
from stitch_generator.shapes.circle import circle_shape
from stitch_generator.stitch_operations.smooth import smooth
from tests.functions.functions import all_functions


def test_smooth():
    # apply smoothing on values of 1d and 2d functions
    for name, f in all_functions.items():
        stitches = f(subdivide_by_number(10))
        result = smooth(stitches=stitches, iterations=5, neighbor_weight=0.5)

        # check that smoothing preserves the start and end stitch
        assert np.allclose(stitches[0], result[0])
        assert np.allclose(stitches[-1], result[-1])

        # check that smoothing keeps the number of stitches unchanged.
        assert len(stitches) == len(result)


def test_smooth_special_cases():
    # only two stitches
    stitches = np.array(((0, 0), (10, 0)))
    result = smooth(stitches=stitches, iterations=5, neighbor_weight=0.5)
    assert np.allclose(result, stitches)

    # circular
    shape = circle_shape(radius=10)
    stitches = shape(subdivide_by_number(30))
    result = smooth(stitches=stitches, iterations=5, neighbor_weight=0.5, circular=True)

    # check that start and end points have changed
    assert not np.allclose(result[0], stitches[0])
    assert not np.allclose(result[-1], stitches[-1])
