import numpy as np

from stitch_generator.functions.ensure_shape import ensure_2d_shape
from stitch_generator.stitch_operations.remove_duplicates import remove_duplicates


def test_remove_duplicates():
    # start duplicate
    stitches = np.array(((0, 0), (0, 0), (10, 0), (20, 0)))
    result = remove_duplicates(stitches)
    assert np.allclose(result, ((0, 0), (10, 0), (20, 0)))

    # middle duplicate
    stitches = np.array(((0, 0), (10, 0), (10, 0), (20, 0)))
    result = remove_duplicates(stitches)
    assert np.allclose(result, ((0, 0), (10, 0), (20, 0)))

    # end duplicate
    stitches = np.array(((0, 0), (10, 0), (20, 0), (20, 0)))
    result = remove_duplicates(stitches)
    assert np.allclose(result, ((0, 0), (10, 0), (20, 0)))

    # multiple duplicates
    stitches = np.array(((0, 0), (10, 0), (10, 0), (10, 0), (10, 0), (20, 0)))
    result = remove_duplicates(stitches)
    assert np.allclose(result, ((0, 0), (10, 0), (20, 0)))

    # no duplicate
    stitches = np.array(((0, 0), (10, 0), (20, 0)))
    result = remove_duplicates(stitches)
    assert np.allclose(result, stitches)

    # one stitch
    stitches = ensure_2d_shape(np.array(((0, 0))))
    result = remove_duplicates(stitches)
    assert np.allclose(result, stitches)
