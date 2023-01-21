from itertools import product

import numpy as np
import pytest

from stitch_generator.subdivision.subdivide_by_fixed_length import subdivision_by_fixed_length

segment_lengths = [0.01, 1, 2, 10]
total_lengths = [0.5, 1, 5.5, 10, 99]
test_values = list(product(total_lengths, segment_lengths))


@pytest.mark.parametrize("total_length, segment_length", test_values)
def test_subdivision_by_fixed_length(total_length, segment_length):
    # create subdivision function
    subdivision = subdivision_by_fixed_length(segment_length=segment_length)

    # subdivide the total length
    values = subdivision(total_length)

    # expect that all values are above or equal to zero
    assert np.alltrue(values >= 0)

    # expect that all values are below or equal to one
    assert np.alltrue(values <= 1)

    # if there are multiple values, check that their distance is always segment_length
    if len(values) > 1:
        # scale values from range [0,1] to [0, total_length]
        values *= total_length

        # calculate the difference between each value and its predecessor
        delta = values[1:] - values[:-1]

        # check if the differences are all equal to segment-length
        assert np.allclose(delta, segment_length)


@pytest.mark.parametrize("total_length", total_lengths)
def test_subdivide_by_fixed_length_segment_zero(total_length):
    """ Test subdividing with a segment length of zero """
    subdivision = subdivision_by_fixed_length(segment_length=0)

    # subdivide the total length
    values = subdivision(total_length)

    # check that a segment length of zero returns the start and end value
    assert np.allclose(values, np.array((0, 1)))


@pytest.mark.parametrize("segment_length", segment_lengths)
def test_subdivide_by_fixed_length_total_zero(segment_length):
    """ Test subdivision with a total length of zero """
    subdivision = subdivision_by_fixed_length(segment_length=segment_length)

    # subdivide the total length
    values = subdivision(0)

    # check that a total length of zero returns the start and end value
    assert np.allclose(values, np.array((0, 1)))
