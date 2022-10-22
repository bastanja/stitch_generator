import numpy as np

from stitch_generator.sampling.resample import resample, resample_with_sampling_function, resample_by_segment
from stitch_generator.sampling.sample_by_fixed_length import sampling_by_fixed_length
from stitch_generator.sampling.sample_by_length import sampling_by_length
from stitch_generator.sampling.sample_by_number import sample_by_number, sampling_by_number
from stitch_generator.shapes.line import line_shape


def test_resample():
    f = line_shape((0, 0), (10, 0))
    stitches = f(sample_by_number(10))

    resampled = resample(stitches, 2)
    assert len(resampled) == 6
    assert np.allclose(resampled, f(sample_by_number(5)))

    resampled = resample(stitches, 0.2)
    assert len(resampled) == 51
    assert np.allclose(resampled, f(sample_by_number(50)))


def sampling_functions():
    yield sampling_by_length(segment_length=3)
    yield sampling_by_fixed_length(segment_length=2, alignment=0, offset=0)
    yield sampling_by_number(number_of_segments=3)


def test_resample_with_sampling_function():
    total_length = 10

    f = line_shape((0, 0), (total_length, 0))
    stitches = f(sample_by_number(100))

    for sampling_function in iter(sampling_functions()):
        direct_samples = f(sampling_function(total_length))
        resampled = resample_with_sampling_function(stitches, sampling_function)
        assert np.allclose(direct_samples, resampled)


def test_resample_by_segment():
    polyline = ((0, 50), (0, 0), (50, 0))
    result = resample_by_segment(points=polyline, segment_length=10)
    length = result.shape[0]
    assert length == 11
    assert np.allclose(result[0], polyline[0])
    assert np.allclose(result[5], polyline[1])
    assert np.allclose(result[-1], polyline[-1])
