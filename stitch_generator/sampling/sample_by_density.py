import numpy as np
from scipy.interpolate import interp1d

from stitch_generator.functions.functions_1d import linear_interpolation
from stitch_generator.sampling.sample_by_length import sample_by_length
from stitch_generator.utilities.types import SamplingFunction, Array1D, Function1D


def sample_by_density(total_length: float, segment_length: float, density_distribution: Function1D,
                      include_endpoint: bool) -> Array1D:
    density_function, sample_ratio = _inverse_cdf(density_distribution)

    samples = density_function(sample_by_length(total_length=total_length * sample_ratio, segment_length=segment_length,
                                                include_endpoint=include_endpoint))

    # handle case where the density is zero
    if not np.isclose(samples[-1], 1) and include_endpoint:
        samples = np.append(samples, 1)

    return samples


def sampling_by_density(segment_length: float, density_distribution: Function1D,
                        include_endpoint: bool) -> SamplingFunction:
    def f(total_length: float):
        return sample_by_density(total_length=total_length, segment_length=segment_length,
                                 density_distribution=density_distribution, include_endpoint=include_endpoint)

    return f


def _inverse_cdf(f, num_approximation_samples: int = 200):
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

    # handle case where the density is zero
    if np.allclose(y_values, 0):
        return linear_interpolation(0, 1), 0

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
