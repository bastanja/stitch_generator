from scipy.interpolate import interp1d

from stitch_generator.functions.estimate_length import accumulate_lengths
from stitch_generator.functions.samples import linspace


def sample(function, number_of_samples: int, include_endpoint: bool = True):
    v = linspace(0, 1, number_of_segments=number_of_samples, include_endpoint=include_endpoint)
    return function(v)


def sample_by_length(function, stitch_length, include_endpoint: bool = True):
    mapping, total_length = length_to_parameter_mapping(function)
    num_samples = int(round(total_length / stitch_length))
    num_samples = max(1, num_samples)
    lengths = linspace(0, total_length, number_of_segments=num_samples, include_endpoint=include_endpoint)
    parameters = mapping(lengths)
    return function(parameters)


def length_to_parameter_mapping(function, approximation_samples=1000):
    parameters = linspace(0, 1, number_of_segments=approximation_samples, include_endpoint=True)
    accumulated = accumulate_lengths(function(parameters))
    length_to_parameter = interp1d(accumulated, parameters)
    return length_to_parameter, accumulated[-1]


def arc_length_mapping(function, approximation_samples=1000):
    return arc_length_mapping_with_length(function, approximation_samples)[0]


def arc_length_mapping_with_length(function, approximation_samples=1000):
    parameters = linspace(0, 1, number_of_segments=approximation_samples, include_endpoint=True)
    accumulated = accumulate_lengths(function(parameters))
    length = accumulated[-1]
    accumulated /= length
    length_to_parameter = interp1d(accumulated, parameters)
    return length_to_parameter, length


def resample(stitches, stitch_length):
    """
    Returns stitches which lie the polyline defined by the parameter stitches. The newly calculated stitches have
    approximately the distance stitch_length. This function can be used to increase or decrease the stitch density.
    """
    accumulated = accumulate_lengths(stitches)
    accumulated /= accumulated[-1]

    # create interpolation function between stitches
    interpolation = interp1d(accumulated, stitches, kind='linear', axis=0)

    return sample_by_length(interpolation, stitch_length)
