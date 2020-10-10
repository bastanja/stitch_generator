import numpy as np

from stitch_generator.functions.functions_2d import line
from stitch_generator.functions.resample import resample
from stitch_generator.functions.samples import samples_by_segments


def sample(f, num_segments, include_endpoint):
    return f(samples_by_segments(number_of_segments=num_segments, include_endpoint=include_endpoint))


def test_resample():
    f = line((0, 0), (10, 0))
    stitches = sample(f, 10, True)

    resampled = resample(stitches, 2)
    assert len(resampled) == 6
    assert np.allclose(resampled, sample(f, 5, True))

    resampled = resample(stitches, 0.2)
    assert len(resampled) == 51
    assert np.allclose(resampled, sample(f, 50, True))
