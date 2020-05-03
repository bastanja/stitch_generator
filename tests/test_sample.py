import numpy as np
from lib.functions_1d import linear_interpolation, sinus, noise
from lib.functions_2d import line, circle
from lib.sample import sample, resample

functions = [linear_interpolation(1, 2), sinus(), noise(), circle(), line(10, 20)]


def test_sample():
    samples = 10
    for f in functions:
        points_with_endpoint = sample(f, samples)
        assert len(points_with_endpoint) == samples + 1
        assert np.allclose(points_with_endpoint[0], f(0))
        assert np.allclose(points_with_endpoint[-1], f(1))

        points_without_endpoint = sample(f, samples, False)
        assert len(points_without_endpoint) == samples
        assert np.allclose(points_without_endpoint[-1], points_with_endpoint[-2])

        assert isinstance(points_with_endpoint, np.ndarray)


def test_resample():
    f = line(10, 0)
    stitches = sample(f, 10, True)

    resampled = resample(stitches, 2)
    assert len(resampled) == 6
    assert np.allclose(resampled, sample(f, 5, True))

    resampled = resample(stitches, 0.2)
    assert len(resampled) == 51
    assert np.allclose(resampled, sample(f, 50, True))
