from scipy.interpolate import interp1d

from stitch_generator.functions.estimate_length import accumulate_lengths
from stitch_generator.sampling.sample_by_number import sample_by_number


def length_to_parameter_mapping(function, approximation_samples=1000):
    parameters = sample_by_number(number_of_segments=approximation_samples, include_endpoint=True)
    accumulated = accumulate_lengths(function(parameters))
    length_to_parameter = interp1d(accumulated, parameters)
    return length_to_parameter, accumulated[-1]


def arc_length_mapping(function, approximation_samples=1000):
    return arc_length_mapping_with_length(function, approximation_samples)[0]


def arc_length_mapping_with_length(function, approximation_samples=1000):
    parameters = sample_by_number(number_of_segments=approximation_samples, include_endpoint=True)
    accumulated = accumulate_lengths(function(parameters))
    length = accumulated[-1]
    accumulated /= length
    length_to_parameter = interp1d(accumulated, parameters)
    return length_to_parameter, length
