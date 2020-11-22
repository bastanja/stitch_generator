from scipy.interpolate import interp1d

from stitch_generator.functions.estimate_length import accumulate_lengths
from stitch_generator.functions.function_modifiers import combine
from stitch_generator.utilities.types import Function2D, Function1D
from stitch_generator.sampling.sample_by_number import sample_by_number


def parameterize_by_arc_length(function: Function2D, approximation_samples: int = 1000) -> Function2D:
    """
    Reparameterizes a 2D function in such a way that the parameter 0.5 returns the geometrical middle point of the
    geometry defined by the 2D function. When calling the reparameterized function with equally spaced samples, the
    resulting positions are approximately equally spaced

    Args:
        function:              The 2D function to reparameterize
        approximation_samples: The number of samples to use for the approximation

    Returns:
        The reparameterized 2D function
    """
    mapping = arc_length_mapping(function, approximation_samples)
    return combine(mapping, function)


def arc_length_mapping(function: Function2D, approximation_samples: int = 1000) -> Function1D:
    """
    Calculates the arc length parameterization for a given 2D function.

    Args:
        function:              The 2D function for which the parameterization is calculated
        approximation_samples: The number of samples to use for the approximation

    Returns:
        A 1D function that maps each parameter in range [0, 1] to its arc length parameterized value in range [0, 1]
    """
    return arc_length_mapping_with_length(function, approximation_samples)[0]


def arc_length_mapping_with_length(function: Function2D, approximation_samples=1000):
    """
    Calculates the arc length parameterization for a given 2D function and the length of the geometry described by the
    2D function

    Args:
        function:              The 2D function for which the parameterization is calculated
        approximation_samples: The number of samples to use for the approximation

    Returns:
        A 1D function that maps each parameter in range [0, 1] to its arc length parameterized value in range [0, 1]
        and the approximated length of the 2D function
    """
    parameters = sample_by_number(number_of_segments=approximation_samples, include_endpoint=True)
    accumulated = accumulate_lengths(function(parameters))
    length = accumulated[-1]
    accumulated /= length
    length_to_parameter = interp1d(accumulated, parameters)
    return length_to_parameter, length
