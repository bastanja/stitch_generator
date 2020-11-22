import numpy as np

from stitch_generator.sampling.sample_by_density import _inverse_cdf
from tests.functions import functions_1d_positive


def test_inverse_cdf():
    for name, f in functions_1d_positive.items():
        icdf, area = _inverse_cdf(f)
        # Area should be between 0 and 1
        assert 0 < area <= 1

        # Evaluate the inverse cumulative distribution function
        v = icdf(np.linspace(0, 1, 100))

        # Values should be in ascending order. Verify it by comparing values to sorted values
        assert np.allclose(v, np.sort(v))

        # First value should be 0, last value should be 1
        assert np.allclose(v[0], 0)
        assert np.allclose(v[-1], 1)
