import numpy as np

from stitch_generator.sampling.sample_by_fixed_length import sampling_by_fixed_length


def _test_sample_by_fixed_length(total_length, segment_length, expected_segments, include_endpoint):
    sampling = sampling_by_fixed_length(segment_length=segment_length, include_endpoint=include_endpoint)
    samples = sampling(total_length)

    segment_length_relative = 0
    if total_length > 0:
        segment_length_relative = segment_length / total_length

    reference = [segment_length_relative * i for i in range(expected_segments + 1)]

    assert len(samples) == expected_segments + 1
    assert np.allclose(samples, reference)


def test_sample_by_fixed_length():
    # test where segments fit into length exactly
    _test_sample_by_fixed_length(total_length=10, segment_length=2, expected_segments=5, include_endpoint=True)
    _test_sample_by_fixed_length(total_length=10, segment_length=2, expected_segments=4, include_endpoint=False)

    _test_sample_by_fixed_length(total_length=12, segment_length=2, expected_segments=6, include_endpoint=True)
    _test_sample_by_fixed_length(total_length=12, segment_length=2, expected_segments=5, include_endpoint=False)

    # test with partial segment
    _test_sample_by_fixed_length(total_length=9.99, segment_length=2, expected_segments=4, include_endpoint=False)
    _test_sample_by_fixed_length(total_length=10.01, segment_length=2, expected_segments=5, include_endpoint=False)
    _test_sample_by_fixed_length(total_length=11.99, segment_length=2, expected_segments=5, include_endpoint=False)

    # test with segment length which is larger than the total length
    _test_sample_by_fixed_length(total_length=5, segment_length=10, expected_segments=0, include_endpoint=False)

    # test with total length of zero
    _test_sample_by_fixed_length(total_length=0, segment_length=10, expected_segments=0, include_endpoint=False)

    # test with segment length of zero
    _test_sample_by_fixed_length(total_length=5, segment_length=0, expected_segments=0, include_endpoint=False)
