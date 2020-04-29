from functools import partial
import numpy as np
from scipy.interpolate import interp1d


def sample(function, number_of_samples: int, include_endpoint: bool = True):
    if include_endpoint:
        number_of_samples += 1
    v = np.linspace(0, 1, num=number_of_samples, endpoint=include_endpoint)
    return np.array([function(t) for t in v])


def sample_by_length(function, stitch_length, include_endpoint: bool = True):
    mapping, total_length = get_length_to_parameter_mapping(function)
    num_samples = int(total_length / stitch_length)
    num_samples = max(num_samples, 1) + 1
    lengths = np.linspace(0, total_length, num_samples)
    parameters = mapping(lengths)
    if not include_endpoint:
        parameters = parameters[0:-1]
    return function(parameters)


def get_length_to_parameter_mapping(function, approximation_samples=1000):
    parameters, accumulated = _accumulate_lengths(function, approximation_samples)
    length_to_parameter = interp1d(accumulated, parameters)
    return length_to_parameter, accumulated[-1]


def _accumulate_lengths(function, approximation_samples):
    parameters = np.linspace(0, 1, approximation_samples)
    points = function(parameters)

    # calculate and accumulate point distances
    to_previous = points - np.roll(points, 1, 0)
    distance_to_previous = np.linalg.norm(to_previous, axis=1)
    distance_to_previous[0] = 0  # first point has no predecessor, set distance to 0
    accumulated = np.add.accumulate(distance_to_previous)
    return parameters, accumulated


def sample_generator(number_of_samples: int, include_endpoint: bool = True):
    return partial(_generator, number_of_samples=number_of_samples, include_endpoint=include_endpoint)


def middle_sample_generator(number_of_samples: int):
    return partial(_generator_middle, number_of_samples=number_of_samples)


def resample(stitches, stitch_length):
    """
    Returns stitches which lie the polyline defined by the parameter stitches. The newly calculated stitches have
    approximately the distance stitch_length. This function can be used to increase or decrease the stitch density.
    """
    # calculate and accumulate stitch distances
    to_previous = stitches - np.roll(stitches, 1, 0)
    distance_to_previous = np.linalg.norm(to_previous, axis=1)
    distance_to_previous[0] = 0  # first stitch has no predecessor, set distance to 0
    accumulated = np.add.accumulate(distance_to_previous)

    # create interpolation function between stitches
    interpolation = interp1d(accumulated, stitches, kind='linear', axis=0)

    # calculate length values for the new stitches
    total_length = accumulated[-1]
    number_of_stitches = int(round(total_length / stitch_length)) + 1  # + 1: always include the endpoint
    length_values = np.linspace(0, total_length, number_of_stitches, endpoint=True)

    return interpolation(length_values)


def _generator(function, number_of_samples: int, include_endpoint: bool = True):
    step = 1 / number_of_samples

    for i in range(number_of_samples):
        yield function(step * i)

    if include_endpoint:
        yield function(1)


def _generator_middle(function, number_of_samples: int):
    step = 1 / number_of_samples

    for i in range(number_of_samples):
        yield function(step * (i + 0.5))
