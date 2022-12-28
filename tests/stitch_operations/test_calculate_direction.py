import numpy as np
import pytest

from stitch_generator.stitch_operations.calculate_direction import calculate_direction


def test_calculate_direction():
    # collinear stitches
    stitches = np.array(((0, 0), (0, 10), (0, 20)))
    directions = calculate_direction(stitches)
    assert len(directions) == len(stitches)
    assert np.allclose(directions, (1, 0))

    # corner
    stitches = np.array(((0, 10), (0, 0), (10, 0)))
    directions = calculate_direction(stitches)
    assert np.allclose(directions, ((-1, 0), (-1, -1), (0, -1)))

    # corner backwards
    stitches = np.array(((10, 0), (0, 0), (0, 10)))
    directions = calculate_direction(stitches)
    assert np.allclose(directions, ((0, 1), (1, 1), (1, 0)))

    # not circular
    stitches = np.array(((0, 10), (0, 0), (10, 0), (10, 10), (0, 10)))
    directions = calculate_direction(stitches, circular=False)
    assert np.allclose(directions, ((-1, 0), (-1, -1), (1, -1), (1, 1), (0, 1)))

    # circular
    stitches = np.array(((0, 10), (0, 0), (10, 0), (10, 10), (0, 10)))
    directions = calculate_direction(stitches, circular=True)
    assert np.allclose(directions, ((-1, 1), (-1, -1), (1, -1), (1, 1), (-1, 1)))

    # too few stitches
    stitches = (0, 0)
    with pytest.raises(Exception):
        calculate_direction(stitches)

