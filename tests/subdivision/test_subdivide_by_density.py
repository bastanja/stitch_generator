import numpy as np

from stitch_generator.functions.functions_1d import constant
from stitch_generator.subdivision.subdivide_by_density import subdivision_by_density, _inverse_cdf
from stitch_generator.subdivision.subdivide_by_length import subdivision_by_length
from tests.functions.functions import functions_1d_positive

lengths = [0, 0.5, 1, 1.7, 2, 5, 10, 100, 100.5]

segment_lengths = [0, 0.1, 0.55, 1, 2, 6]


def test_constant_density_one():
    """ Test that subdivision with constant density of 1 is the same as regular subdivision """

    density_function = constant(1)

    for segment_length in segment_lengths:
        constant_density = subdivision_by_density(segment_length=segment_length, density_distribution=density_function)
        regular_subdivision = subdivision_by_length(segment_length=segment_length)

        for length in lengths:
            assert np.allclose(constant_density(length), regular_subdivision(length))


def test_constant_density_low():
    """ Test that subdivision with constant density of 0 returns only the start point and the end point """

    density_function = constant(0)

    for segment_length in segment_lengths:
        subdivision = subdivision_by_density(segment_length=segment_length, density_distribution=density_function)

        for length in lengths:
            values = subdivision(length)
            assert np.allclose(values, np.array([0, 1], dtype=float))


def test_varying_density():
    """ Test that subdivision with varying density results in fewer or equal values than regular subdivision """

    for f in functions_1d_positive.values():
        for segment_length in segment_lengths:
            varying_density = subdivision_by_density(segment_length=segment_length, density_distribution=f)
            regular_subdivision = subdivision_by_length(segment_length=segment_length)

            for length in lengths:
                values_varying_density = varying_density(length)
                values_regular_subdivision = regular_subdivision(length)
                assert len(values_varying_density) <= len(values_regular_subdivision)


def test_zero_and_one_included():
    """ Test that density subdivision always includes 0 and 1 """

    for name, f in functions_1d_positive.items():
        for segment_length in segment_lengths:
            subdivision = subdivision_by_density(segment_length=segment_length, density_distribution=f)

            for length in lengths:
                values_varying_density = subdivision(length)
                assert np.isclose(values_varying_density[0], 0)
                assert np.isclose(values_varying_density[-1], 1)


def test_inverse_cdf():
    for name, f in functions_1d_positive.items():
        icdf, area = _inverse_cdf(f)
        # Area should be between 0 and 1
        assert 0 <= area <= 1

        # Evaluate the inverse cumulative distribution function
        v = icdf(np.linspace(0, 1, 100))

        # Values should be in ascending order. Verify it by comparing values to sorted values
        assert np.allclose(v, np.sort(v))

        # First value should be 0, last value should be 1
        assert np.allclose(v[0], 0)
        assert np.allclose(v[-1], 1)
