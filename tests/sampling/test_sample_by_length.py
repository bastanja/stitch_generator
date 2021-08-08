import numpy as np
import pytest

from stitch_generator.sampling.sample_by_length import sample_by_length

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
