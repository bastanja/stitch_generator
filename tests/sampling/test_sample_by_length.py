from itertools import product

import numpy as np
import pytest

from stitch_generator.sampling.sample_by_length import sample_by_length, sampling_by_length_with_offset, regular_even, \
    regular_odd

test_values = [
    # test where segments fit into length exactly
    (10, 2, 5), (12, 2, 6),
    # test with half segment
    (10.49, 2, 5), (11, 2, 6), (11.01, 2, 6),
    # test with segment length which is larger than the total length
    (5, 10, 1)
]


@pytest.mark.parametrize("total_length, segment_length, expected_segments", test_values)
def test_sample_by_length(total_length, segment_length, expected_segments):
    """ Test that sampling returns equally spaced samples of the expected length """
    with_endpoint = sample_by_length(total_length, segment_length)

    reference = [1 / expected_segments * i for i in range(expected_segments + 1)]

    assert len(with_endpoint) == expected_segments + 1
    assert np.allclose(with_endpoint, reference)


@pytest.mark.parametrize("total_length, expected_samples", [(10, [0, 1]), (1, [0, 1]), (0, [0, 1])])
def test_sample_by_length_segment_zero(total_length, expected_samples):
    """ Test sampling with a segment length of zero """
    assert np.allclose(sample_by_length(total_length=total_length, segment_length=0),
                       expected_samples)


@pytest.mark.parametrize("segment_length, expected_samples", [(2, [0, 1])])
def test_sample_by_length_total_zero(segment_length, expected_samples):
    """ Test sampling with a total length of zero """
    assert np.allclose(
        sample_by_length(total_length=0, segment_length=segment_length),
        expected_samples)


def test_sampling_by_length_with_offset():
    # offset of a half segment length
    sampling_function = sampling_by_length_with_offset(segment_length=1, offset=0.5)
    samples = sampling_function(5)
    expected_samples = np.array((0.5, 1.5, 2.5, 3.5, 4.5)) / 5
    assert (np.allclose(samples, expected_samples))

    # offset of a quarter segment length
    sampling_function = sampling_by_length_with_offset(segment_length=1, offset=0.25)
    samples = sampling_function(5)
    expected_samples = np.array((0.25, 1.25, 2.25, 3.25, 4.25)) / 5
    assert (np.allclose(samples, expected_samples))

    # negative offset
    sampling_function = sampling_by_length_with_offset(segment_length=1, offset=-0.5)
    samples = sampling_function(5)
    expected_samples = np.array((0.5, 1.5, 2.5, 3.5, 4.5)) / 5
    assert (np.allclose(samples, expected_samples))

    # offset above 1
    sampling_function = sampling_by_length_with_offset(segment_length=1, offset=2.2)
    samples = sampling_function(3)
    expected_samples = np.array((0.2, 1.2, 2.2)) / 3
    assert (np.allclose(samples, expected_samples))

    # segment length longer than total length
    sampling_function = sampling_by_length_with_offset(segment_length=10, offset=0.1)
    samples = sampling_function(5)
    expected_samples = np.array((1)) / 5
    assert (np.allclose(samples, expected_samples))


segment_lengths = [0.01, 1, 2, 10]
total_lengths = [0.5, 1, 5.5, 10, 99]
test_values = list(product(total_lengths, segment_lengths))


@pytest.mark.parametrize("total_length, segment_length", test_values)
def test_regular_even(total_length, segment_length):
    sampling_function = regular_even(segment_length=segment_length)
    samples = sampling_function(total_length)
    assert len(samples) % 2 == 0


@pytest.mark.parametrize("total_length, segment_length", test_values)
def test_regular_odd(total_length, segment_length):
    sampling_function = regular_odd(segment_length=segment_length)
    samples = sampling_function(total_length)
    assert len(samples) % 2 == 1
