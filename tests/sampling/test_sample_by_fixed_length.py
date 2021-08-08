import numpy as np

from stitch_generator.sampling.sample_by_fixed_length import sampling_by_fixed_length


def _test_sample_by_fixed_length(total_length, segment_length, expected_segments):
    sampling = sampling_by_fixed_length(segment_length=segment_length)
    samples = sampling(total_length)

    segment_length_relative = 0
    if total_length > 0:
        segment_length_relative = segment_length / total_length

    reference = [segment_length_relative * i for i in range(expected_segments + 1)]

    assert len(samples) == expected_segments + 1
    assert np.allclose(samples, reference)


def test_sample_by_fixed_length():
    _test_sample_by_fixed_length(total_length=10, segment_length=2, expected_segments=5)
    _test_sample_by_fixed_length(total_length=12, segment_length=2, expected_segments=6)
