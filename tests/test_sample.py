import numpy as np
from lib.functions_1d import linear_interpolation, sinus, noise
from lib.functions_2d import line, circle
from lib.sample import sample, sample_generator, middle_sample_generator

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


def test_sample_generator():
    samples = 10
    with_endpoint = True
    gen = sample_generator(samples, with_endpoint)

    # check that sample_generator returns a generator function
    for f in functions:
        f_gen = gen(f)
        v = next(f_gen)
        assert np.allclose(v, f(0))

    # check that the sample generator returns the same as the sample function
    for f in functions:
        # generate a list with the generator
        f_gen = gen(f)
        v1 = list(f_gen)

        # retrieve a list from the sample function
        v2 = sample(f, samples, with_endpoint)

        assert np.allclose(v1, v2)


def test_middle_sample_generator():
    samples = 10
    mid = middle_sample_generator(samples)

    f = linear_interpolation(0, 20)
    assert np.allclose(list(mid(f)), (1, 3, 5, 7, 9, 11, 13, 15, 17, 19))
