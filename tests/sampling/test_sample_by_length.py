import numpy as np

from stitch_generator.sampling.sample_by_length import sample_by_length


def _test_sample_by_length(total_length, segment_length, expected_segments):
    with_endpoint = sample_by_length(total_length, segment_length, include_endpoint=True)
    no_endpoint = sample_by_length(total_length, segment_length, include_endpoint=False)

    if expected_segments is 0:
        assert len(with_endpoint) == 1
        assert len(no_endpoint) == 1
    else:
        reference = [1 / expected_segments * i for i in range(expected_segments + 1)]

        assert len(with_endpoint) == expected_segments + 1
        assert len(no_endpoint) == expected_segments
        assert np.allclose(with_endpoint[:-1], no_endpoint)
        assert np.allclose(with_endpoint, reference)


def test_samples_by_length():
    # test where segments fit into length exactly
    _test_sample_by_length(total_length=10, segment_length=2, expected_segments=5)
    _test_sample_by_length(total_length=12, segment_length=2, expected_segments=6)

    # test with half segment
    _test_sample_by_length(total_length=10.49, segment_length=2, expected_segments=5)
    _test_sample_by_length(total_length=11, segment_length=2, expected_segments=6)
    _test_sample_by_length(total_length=11.01, segment_length=2, expected_segments=6)

    # test with segment length which is larger than the total length
    _test_sample_by_length(total_length=5, segment_length=10, expected_segments=1)

    # test with total length of zero
    _test_sample_by_length(total_length=0, segment_length=10, expected_segments=0)

    # test with segment length of zero
    _test_sample_by_length(total_length=5, segment_length=0, expected_segments=1)
