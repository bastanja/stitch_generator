from lib.functions_1d import *
from lib.inverse_cdf import inverse_cdf


def test_inverse_cdf():
    functions = [linear_interpolation(0, 1), constant(0), sinus(), cosinus(), noise(),
                        cubic_interpolation_evenly_spaced([0, 1, 0]), stairs(5, 0.1), square(), arc(),
                        smoothstep(), smootherstep(), circular_arc()]

    for i, f in enumerate(functions):
        print(i)

        icdf, area = inverse_cdf(f)
        # Area should be between 0 and 1
        assert 0 < area <= 1

        # Evaluate the inverse cumulative distribution function
        v = icdf(np.linspace(0, 1, 100))

        # Values should be in ascending order. Verify it ba comparing values to sorted values
        assert np.allclose(v, np.sort(v))

        # First value should be 0, last value should be 1
        assert np.allclose(v[0], 0)
        assert np.allclose(v[-1], 1)
