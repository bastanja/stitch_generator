import numpy as np
from noise import pnoise2

from stitch_generator.functions.function_modifiers import shift
from stitch_generator.functions.functions_1d import linear_interpolation, constant, function_1d
from stitch_generator.functions.functions_2d import function_2d
from stitch_generator.stitch_operations.rotate import rotation_by_degrees
from stitch_generator.utilities.types import Function1D, Function2D


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
        rotated = rotation_by_degrees(to_2d, constant(angle))
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
