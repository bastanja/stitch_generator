import itertools

import numpy as np
import pytest

from stitch_generator.functions.connect_functions import running_stitch_line


def test_running_stitch_line():
    start_points = ((0, 0), (0, 10), (20, 20))
    end_points = ((10, 0), (30, 10), (0, 20))
    stitch_lengths = (1, 2, 4, 10)

    # Calculate a running stitch for various start and end points with various stitch lengths
    for stitch_length in stitch_lengths:
        stitch_effect = running_stitch_line(stitch_length=stitch_length, include_endpoint=True)
        point_pairs = itertools.product(start_points, end_points)
        for p in point_pairs:
            expected_length = np.linalg.norm(np.array(p[1]) - np.array(p[0]))
            expected_length = int(round(expected_length / stitch_length)) + 1

            s = stitch_effect(p[0], p[1])
            assert len(s) == expected_length

    # Check that a stitch length of zero results in a stitch at the start and one at the end
    stitch_effect = running_stitch_line(stitch_length=0, include_endpoint=True)
    s = stitch_effect((0, 0), (10, 10))
    assert len(s) == 2
    assert np.allclose(s, ((0, 0), (10, 10)))

    # check that running stitch line of length 0 has only a single point
    stitch_effect = running_stitch_line(stitch_length=1, include_endpoint=True)
    s = stitch_effect((0, 0), (0, 0))
    assert len(s) == 1

    # check that running stitch line has at least a start point
    stitch_effect = running_stitch_line(stitch_length=1, include_endpoint=False)
    s = stitch_effect((0, 0), (0, 0))
    assert len(s) == 1
