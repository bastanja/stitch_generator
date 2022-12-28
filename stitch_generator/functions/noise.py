import numpy as np
from noise import pnoise2

from stitch_generator.framework.types import Function1D, Function2D, Array2D
from stitch_generator.functions.ensure_shape import ensure_2d_shape
from stitch_generator.functions.function_modifiers import shift, repeat, chain
from stitch_generator.functions.functions_1d import linear_interpolation, function_1d, smootherstep
from stitch_generator.functions.functions_2d import function_2d
from stitch_generator.shapes.line import line_shape
from stitch_generator.stitch_operations.rotate import rotate_by_degrees


def noise(octaves: int = 4, angle=20, scale=1) -> Function1D:
    """
    Returns a 1D noise function (input 1D, output 1D)

    Args:
        octaves: the number of passes for generating fBm noise, see pnoise2
        angle: rotation angle which is applied to avoid the zero-values at integer grid of perlin noise
        scale: lower values decrease the density of the noise, higher values increase it

    Returns:
        A Function1D that maps the input value to its noise value

    """

    end_point = rotate_by_degrees(ensure_2d_shape((scale, 1)), angle_deg=angle)
    to_texture_space = line_shape(to=end_point)

    def f(v):
        request_positions = to_texture_space(v)
        return _noise_2d_texture_space(positions_texture_space=request_positions, octaves=octaves)

    return function_1d(f)


def noise_vectors(x_offset=0, y_offset=0, octaves: int = 4, angle=30, scale=1) -> Function2D:
    """
    Returns a 2D noise function (input 1D, output 2D)

    Args:
        x_offset: shift amount along the noise in x-direction
        y_offset: shift amount along the noise in y-direction
        octaves: the number of passes for generating fBm noise, see pnoise2
        angle: rotation angle which is applied to avoid the zero-values at integer grid of perlin noise
        scale: lower values decrease the density of the noise, higher values increase it

    Returns:
        A Function2D that maps the input value to its 2D noise vector

    """
    fx = shift(x_offset, noise(octaves, angle, scale))
    fy = shift(y_offset, noise(octaves, -angle, scale))
    return function_2d(fx, fy)


def noise_field(left, top, right, bottom, octaves: int):
    """
    Returns a noise field function (input 2D, output 1D)

    Args:
        left: left coordinate of the noise field
        top: top coordinate of the noise field
        right: right coordinate of the noise field
        bottom: bottom coordinate of the noise field
        octaves: the number of passes for generating fBm noise, see pnoise2

    Returns:
        A Function2D that maps the input coordinate value to its noise value in the noise

    """

    def f(positions: Array2D):
        """
        Returns a noise value for each position in positions_normalized
        Args:
            positions: Request positions with x and y coordinates in the range [0,1]

        Returns:
            A float value for each request position
        """
        request_positions = _scale_request_positions(positions, left, top, right, bottom)
        return _noise_2d_texture_space(positions_texture_space=request_positions, octaves=octaves)

    return f


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


def _noise_2d_texture_space(positions_texture_space: Array2D, octaves: int):
    return np.array([pnoise2(x=p[0], y=p[1], octaves=octaves) for p in positions_texture_space])


def _scale_request_positions(uv, left, top, right, bottom):
    x_interpolation = linear_interpolation(left, right)
    y_interpolation = linear_interpolation(top, bottom)
    result = uv.copy()
    result[:, 0] = x_interpolation(uv[:, 0])
    result[:, 1] = y_interpolation(uv[:, 1])
    return result
