from itertools import product

import numpy as np
import pytest

from stitch_generator.sampling.sample_by_fixed_length import sampling_by_fixed_length

segment_lengths = [0.01, 1, 2, 10]
total_lengths = [0.5, 1, 5.5, 10, 99]
test_values = list(product(total_lengths, segment_lengths))


@pytest.mark.parametrize("total_length, segment_length", test_values)
def test_sample_by_fixed_length(total_length, segment_length):
    # create sampling function
    sampling = sampling_by_fixed_length(segment_length=segment_length)

    # sample the total length
    samples = sampling(total_length)

    # expect that all samples are greater than zero or equal to zero
    assert np.alltrue(samples >= 0)

    # expect that all samples are below 1
    assert np.alltrue(samples <= 1)

    # if there are multiple samples, check that their distance is always segment_length
    if len(samples) > 1:
        # scale samples from range [0,1] to [0, total_length]
        samples *= total_length

        # calculate the difference between each sample and its predecessor
        delta = samples[1:] - samples[:-1]

        # check if the differences are all equal to segment-length
        assert np.allclose(delta, segment_length)


@pytest.mark.parametrize("total_length", total_lengths)
def test_sample_by_fixed_length_segment_zero(total_length):
    """ Test sampling with a segment length of zero """
    sampling = sampling_by_fixed_length(segment_length=0)

    # sample the total length
    samples = sampling(total_length)

    # check that a segment length of zero returns the start and end sample
    assert np.allclose(samples, np.array((0, 1)))


@pytest.mark.parametrize("segment_length", segment_lengths)
def test_sample_by_fixed_length_total_zero(segment_length):
    """ Test sampling with a total length of zero """
    sampling = sampling_by_fixed_length(segment_length=segment_length)

    # sample the total length
    samples = sampling(0)

    # check that a total length of zero returns the start and end sample
    assert np.allclose(samples, np.array((0, 1)))
