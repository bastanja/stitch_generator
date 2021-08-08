import numpy as np

from stitch_generator.functions.functions_1d import constant
from stitch_generator.sampling.sample_by_density import sampling_by_density
from stitch_generator.sampling.sample_by_length import sampling_by_length
from tests.functions import functions_1d_positive

lengths = [0.5, 1, 1.7, 2, 5, 10, 100, 100.5]

segment_lengths = [0, 0.1, 0.55, 1, 2, 6]


def test_constant_density_one():
    """ Test that sampling with constant density of 1 is the same as regular sampling """

    density_function = constant(1)

    for segment_length in segment_lengths:
        constant_density = sampling_by_density(segment_length=segment_length, density_distribution=density_function)
        regular_sampling = sampling_by_length(segment_length=segment_length)

        for length in lengths:
            assert np.allclose(constant_density(length), regular_sampling(length))


def test_constant_density_low():
    """ Test that sampling with constant density of 0 returns only the start point and the end point """

    density_function = constant(0)

    for segment_length in segment_lengths:
        with_endpoint = sampling_by_density(segment_length=segment_length, density_distribution=density_function)

        for length in lengths:
            samples_with_endpoint = with_endpoint(length)
            assert np.allclose(samples_with_endpoint, np.array([0, 1], dtype=float))


def test_varying_density():
    """ Test that sampling with varying density results in fewer or equal samples than regular sampling """

    for f in functions_1d_positive.values():
        for segment_length in segment_lengths:
            varying_density = sampling_by_density(segment_length=segment_length, density_distribution=f)
            regular_sampling = sampling_by_length(segment_length=segment_length)

            for length in lengths:
                samples_varying_density = varying_density(length)
                samples_regular_sampling = regular_sampling(length)
                assert len(samples_varying_density) <= len(samples_regular_sampling)


def test_zero_and_one_included():
    """ Test that density sampling always includes 0 and 1 """

    for name, f in functions_1d_positive.items():
        for segment_length in segment_lengths:
            sampling = sampling_by_density(segment_length=segment_length, density_distribution=f)

            for length in lengths:
                samples_varying_density = sampling(length)
                assert np.isclose(samples_varying_density[0], 0)
                assert np.isclose(samples_varying_density[-1], 1)
