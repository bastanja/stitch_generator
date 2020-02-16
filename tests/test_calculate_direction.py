import math

import numpy as np
import pytest

from lib.calculate_direction import calculate_direction


def test_calculate_direction():
    # test with two stitches
    stitches = ((0.0, 0), (10, 0))
    directions = calculate_direction(stitches)
    assert np.allclose(directions, ((0, -1), (0, -1)))

    # test with three stitches
    stitches = ((0, 0), (10, 0), (20, 0))
    directions = calculate_direction(stitches)
    assert np.allclose(directions, ((0, -1), (0, -1), (0, -1)))

    # test with four stitches
    stitches = ((0, 0), (10, 0), (20, 0), (30, 0))
    directions = calculate_direction(stitches)
    assert np.allclose(directions, ((0, -1), (0, -1), (0, -1), (0, -1)))

    # test with too few stitches
    stitches = (0, 0)
    with pytest.raises(Exception):
        calculate_direction(stitches)

    # test with opposite direction
    stitches = ((30, 0), (20, 0), (10, 0), (0, 0))
    directions = calculate_direction(stitches)
    assert np.allclose(directions, ((0, 1), (0, 1), (0, 1), (0, 1)))

    # test with vertical line
    stitches = ((0, 0), (0, 10), (0, 20), (0, 30))
    directions = calculate_direction(stitches)
    assert np.allclose(directions, ((1, 0), (1, 0), (1, 0), (1, 0)))

    # test with angle
    stitches = np.array(((0, 10), (0, 0), (10, 0)))
    directions = calculate_direction(stitches)
    assert np.allclose(directions, np.array(((-1, 0), (-1, -1), (0, -1))))

    # test with angle in other direction
    stitches = np.array(((0, -10), (0, 0), (10, 0)))
    directions = calculate_direction(stitches)
    assert np.allclose(directions, np.array(((1, 0), (1, -1), (0, -1))))

    # tests with diagonal lines
    length = 1 / math.sqrt(2)

    stitches = ((0, 0), (10, 10), (20, 20), (30, 30))
    directions = calculate_direction(stitches)
    expected_result = np.array([length, -length] * len(stitches)).reshape(len(stitches), 2)
    assert np.allclose(directions, expected_result)

    stitches = ((0, 0), (10, -10), (20, -20), (30, -30))
    directions = calculate_direction(stitches)
    expected_result = np.array([-length, -length] * len(stitches)).reshape(len(stitches), 2)
    assert np.allclose(directions, expected_result)
