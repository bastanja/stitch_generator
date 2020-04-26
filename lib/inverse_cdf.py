import numpy as np
from scipy.interpolate import interp1d


def inverse_cdf(f, num_approximation_samples: int = 200):
    """
    Returns the approximation of a inverse cumulative distribution function for a given function f.
    f must map a scalar x to a scalar y. f must be defined in the range [0,1], the resulting y values may be in the
    range [0,1]

    A higher value for num_approximation_samples increases the accuracy of the approximation.
    """

    # The cumulative distribution function can only be reversed, when it is strictly monotonic increasing. Therefore,
    # we map the y-values to a range [epsilon, 1] and avoid the value 0.
    epsilon = 1.0e-10

    # Evaluate the function at fixed intervals and accumulate the values
    y_values = f(np.linspace(0.0, 1, num_approximation_samples))
    y_values[y_values < epsilon] = epsilon
    y_values = np.cumsum(y_values)
    area_covered = y_values[-1]  # remember the last value for calculation of the covered area

    # Divide by the highest value to map all y_values to [epsilon, 1] again
    y_values /= y_values[-1]

    # Add a new sample at (0,0) again. Otherwise the function returned by interp1d if not defined over the whole
    # range [0,1]
    y_values = np.insert(y_values, 0, 0)

    # The area covered is the area below the graph of f. It is in the range [0,1] and can be used as factor for the
    # number of samples when sampling the returned cdf
    area_covered = area_covered / num_approximation_samples

    x_values = np.linspace(0.0, 1, len(y_values))

    # Inverse the cumulative distribution function by exchanging x_values and y_values
    return interp1d(x=y_values, y=x_values), area_covered
