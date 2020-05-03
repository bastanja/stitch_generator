import itertools

import numpy as np
import pytest

from stitch_generator.stitch_effects.running_stitch import running_stitch_line


def test_running_stitch_line():
    start_points = ((0, 0), (0, 10), (20, 20))
    end_points = ((10, 0), (30, 10), (0, 20))
    stitch_lengths = (1, 2, 4, 10)

    # Calculate a running stitch for various start and end points with various stitch lengths
    for stitch_length in stitch_lengths:
        point_pairs = itertools.product(start_points, end_points)
        for p in point_pairs:
            expected_length = np.linalg.norm(np.array(p[1]) - np.array(p[0]))
            expected_length = int(round(expected_length / stitch_length)) + 1

            s = running_stitch_line(p[0], p[1], stitch_length, True)
            assert len(s) == expected_length

    # Check that a stitch length of zero raises an exception
    with pytest.raises(Exception):
        running_stitch_line((0, 0), (10, 10), 0, True)

    # check that running stitch line has at least start and end point
    s = running_stitch_line((0, 0), (0, 0), 1, True)
    assert len(s) == 2

    # check that running stitch line has at least a start point
    s = running_stitch_line((0, 0), (0, 0), 1, False)
    assert len(s) == 1