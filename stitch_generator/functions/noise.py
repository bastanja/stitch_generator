import numpy as np
from noise import pnoise2

from stitch_generator.framework.types import Function1D, Function2D
from stitch_generator.functions.function_modifiers import shift, rotate_degrees, repeat, chain
from stitch_generator.functions.functions_1d import linear_interpolation, constant, function_1d, smootherstep
from stitch_generator.functions.functions_2d import function_2d


def noise(octaves: int = 4, angle=20, scale=1) -> Function1D:
    """
    Returns a 1D noise function
    Args:
        octaves: the number of passes for generating fBm noise, see pnoise2
        angle: rotation angle which is applied to avoid the zero-values at integer grid of perlin noise
        scale: lower values decrease the density of the noise, higher values increase it

    Returns:
        A Function1D that maps the input value to its noise value

    """

    def f(v):
        to_2d = function_2d(linear_interpolation(0, scale), constant(0))
        rotated = rotate_degrees(to_2d, constant(angle))
        v2d = rotated(v)
        return np.array([pnoise2(p[0], p[1], octaves=octaves) for p in v2d])

    return function_1d(f)


def noise_2d(x_offset=0, y_offset=0, octaves: int = 4, angle=30, scale=1) -> Function2D:
    """
    Returns a 2D noise function (input 1D, output 2D)
    Args:
        x_offset: shift amount along the noise in x-direction
        y_offset: shift amount along the noise in y-direction
        octaves: the number of passes for generating fBm noise, see pnoise2
        angle: rotation angle which is applied to avoid the zero-values at integer grid of perlin noise
        scale: lower values decrease the density of the noise, higher values increase it

    Returns:
        A Function2D that maps the input value to its 2D noise value

    """
    fx = shift(x_offset, noise(octaves, angle, scale))
    fy = shift(y_offset, noise(octaves, -angle, scale))
    return function_2d(fx, fy)


def fix_distribution(noise_function: Function1D, noise_range: float = 0.35, target_low=-1, target_high=1):
    """
    Spreads the values of the noise function so that they are closer to a uniform distribution

    The values of perlin noise have a distribution that is similar to gaussian normal distribution, i.e. many values
    are near the middle and few are at the borders. Combining it with a cumulative distribution function (CDF), the
    distribution of the values can be changed. Using smootherstep as CDF, the values get distributed more evenly, closer
    to a uniform distribution.

    Args:
        noise_function: A 1D noise function, e.g. perlin noise
        noise_range: Defines the range [-noise_range, noise_range] of the original noise_function in which
            most values lie
        target_low: the lower border which the noise values of the resulting function shall reach
        target_high: the higher border which the noise values of the resulting function shall reach

    Returns:
        A noise function that returns values in the range [lower_boundary, upper_boundary] with a value distribution
        that is closer to uniform distribution, i.e. where the middle values occur less frequently than before and the
        border value occur more frequently than before
    """

    # map range where most values are to [0,1]
    map_range = linear_interpolation(0, 1, source_low=-noise_range, source_high=noise_range)

    # create a function that returns:
    # 0 for values lower than 0,
    # 1 for values above 1 and
    # smootherstep(t) for all values t between 0 and 1
    spread_distribution = repeat(r=1, function=smootherstep, mode='nearest')

    # combine the range mapping and the spreading of the distribution
    distribution_modification = chain(map_range, spread_distribution)

    # map to the desired output range
    distribution_interpolation = chain(distribution_modification, linear_interpolation(target_low, target_high))

    # combine the original noise function with the distribution modification
    return chain(noise_function, distribution_interpolation)
