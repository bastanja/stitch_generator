import numpy as np

from stitch_generator.functions.functions_2d import line
from stitch_generator.sampling.resample import resample, resample_with_sampling_function
from stitch_generator.sampling.sample_by_number import sample_by_number
from stitch_generator.sampling.sampling_presets import sampling_presets_stateless


def test_resample():
    f = line((0, 0), (10, 0))
    stitches = f(sample_by_number(10, include_endpoint=True))

    resampled = resample(stitches, 2)
    assert len(resampled) == 6
    assert np.allclose(resampled, f(sample_by_number(5, include_endpoint=True)))

    resampled = resample(stitches, 0.2)
    assert len(resampled) == 51
    assert np.allclose(resampled, f(sample_by_number(50, include_endpoint=True)))


def test_resample_with_sampling_function():
    total_length = 10

    f = line((0, 0), (total_length, 0))
    stitches = f(sample_by_number(100, include_endpoint=True))

    for sampling_function in iter(sampling_presets_stateless(include_endpoint=True)):
        direct_samples = f(sampling_function(total_length))
        resampled = resample_with_sampling_function(stitches, sampling_function)
        assert np.allclose(direct_samples, resampled)
