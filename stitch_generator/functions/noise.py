import numpy as np
from scipy.interpolate import interp1d

from stitch_generator.framework import Array2D, Function1D, Function2D

from .ensure_shape import ensure_2d_shape
from .function_modifiers import compose, repeat, shift
from .functions_1d import function_1d, linear_interpolation, smootherstep
from .functions_2d import function_2d


def noise(octaves: int = 4, angle=20, scale=1) -> Function1D:
    """
    Returns a 1D noise function (input 1D, output 1D)

    Args:
        octaves: the number of passes for generating fBm noise, see _perlin_noise_2d
        angle: rotation angle which is applied to avoid the zero-values at integer grid of perlin noise
        scale: lower values decrease the density of the noise, higher values increase it

    Returns:
        A Function1D that maps the input value to its noise value

    """

    # calculate coordinate of a point which is at distance scale and angle from the origin
    x = scale * np.cos(angle * np.pi / 180)
    y = scale * np.sin(angle * np.pi / 180)
    end_point = (x, y)

    origin = (0, 0)

    # linear interpolation between the origin and the end point
    to_texture_space = interp1d(
        np.array([0, 1]),
        np.vstack((origin, end_point)),
        fill_value="extrapolate",
        axis=0,
    )

    def f(v):
        request_positions = ensure_2d_shape(to_texture_space(v))
        return _noise_2d_texture_space(
            positions_texture_space=request_positions, octaves=octaves
        )

    return function_1d(f)


def noise_vectors(
    x_offset=0, y_offset=0, octaves: int = 4, angle=30, scale=1
) -> Function2D:
    """
    Returns a 2D noise function (input 1D, output 2D)

    Args:
        x_offset: shift amount along the noise in x-direction
        y_offset: shift amount along the noise in y-direction
        octaves: the number of passes for generating fBm noise, see _perlin_noise_2d
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
        octaves: the number of passes for generating fBm noise, see _perlin_noise_2d

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
        request_positions = _scale_request_positions(
            positions, left, top, right, bottom
        )
        return _noise_2d_texture_space(
            positions_texture_space=request_positions, octaves=octaves
        )

    return f


def fix_distribution(
    noise_function: Function1D, noise_range: float = 0.35, target_low=-1, target_high=1
):
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
    map_range = linear_interpolation(
        0, 1, source_low=-noise_range, source_high=noise_range
    )

    # create a function that returns:
    # 0 for values lower than 0,
    # 1 for values above 1 and
    # smootherstep(t) for all values t between 0 and 1
    spread_distribution = repeat(r=1, function=smootherstep, mode="clamp")

    # combine the range mapping and the spreading of the distribution
    distribution_modification = compose(map_range, spread_distribution)

    # map to the desired output range
    distribution_interpolation = compose(
        distribution_modification, linear_interpolation(target_low, target_high)
    )

    # combine the original noise function with the distribution modification
    return compose(noise_function, distribution_interpolation)


def _noise_2d_texture_space(positions_texture_space: Array2D, octaves: int):
    return _perlin_noise_2d(
        positions_texture_space[:, 0], positions_texture_space[:, 1], octaves=octaves
    )


# The Perlin noise implementation below is a numpy port of pnoise2 from the noise package
# (https://github.com/caseman/noise, MIT license), which is based on Ken Perlin's reference implementation of
# improved noise (https://mrl.cs.nyu.edu/~perlin/noise/). It produces the same values as pnoise2 with default
# arguments for persistence, lacunarity, repeatx, repeaty and base.

# Ken Perlin's reference permutation table
_PERMUTATION = np.array(
    [
        151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53, 194, 233, 7, 225,
        140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23, 190, 6, 148,
        247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32,
        57, 177, 33, 88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175,
        74, 165, 71, 134, 139, 48, 27, 166, 77, 146, 158, 231, 83, 111, 229, 122,
        60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244, 102, 143, 54,
        65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169,
        200, 196, 135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64,
        52, 217, 226, 250, 124, 123, 5, 202, 38, 147, 118, 126, 255, 82, 85, 212,
        207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42, 223, 183, 170, 213,
        119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9,
        129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104,
        218, 246, 97, 228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241,
        81, 51, 145, 235, 249, 14, 239, 107, 49, 192, 214, 31, 181, 199, 106, 157,
        184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205, 93,
        222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180,
    ]
)  # fmt: skip
# the permutation table twice in a row, so that lookups of a table value plus an offset of up to 256 stay in range
_PERMUTATION_DOUBLED = np.concatenate((_PERMUTATION, _PERMUTATION))

# x and y components of the gradient vectors, indexed by the lower 4 bits of the hash value
_GRADIENT_X = np.array([1, -1, 1, -1, 1, -1, 1, -1, 0, 0, 0, 0, 1, -1, 0, 0])
_GRADIENT_Y = np.array([1, 1, -1, -1, 0, 0, 0, 0, 1, -1, 1, -1, 0, 0, -1, 1])

# the grid repeats after this many units, like the default of repeatx and repeaty in pnoise2
_REPEAT = 1024


def _perlin_noise_2d(x, y, octaves: int, persistence=0.5, lacunarity=2.0):
    """
    Returns fractal Brownian motion (fBm) Perlin noise for each pair of x and y coordinates
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    total = np.zeros(np.broadcast(x, y).shape)
    frequency = 1.0
    amplitude = 1.0
    max_amplitude = 0.0

    for _ in range(octaves):
        total += (
            _perlin_noise_2d_single_octave(
                x * frequency, y * frequency, _REPEAT * frequency
            )
            * amplitude
        )
        max_amplitude += amplitude
        frequency *= lacunarity
        amplitude *= persistence

    return total / max_amplitude


def _perlin_noise_2d_single_octave(x, y, repeat):
    # integer grid cell coordinates and the coordinates of the next cell
    i = np.floor(np.fmod(x, repeat)).astype(int)
    j = np.floor(np.fmod(y, repeat)).astype(int)
    ii = np.fmod(i + 1, repeat).astype(int) & 255
    jj = np.fmod(j + 1, repeat).astype(int) & 255
    i &= 255
    j &= 255

    # position inside the grid cell and fade curve values
    x = x - np.floor(x)
    y = y - np.floor(y)
    fx = x * x * x * (x * (x * 6 - 15) + 10)
    fy = y * y * y * (y * (y * 6 - 15) + 10)

    # hash values of the four cell corners
    a = _PERMUTATION_DOUBLED[i]
    b = _PERMUTATION_DOUBLED[ii]
    aa = _PERMUTATION_DOUBLED[a + j]
    ab = _PERMUTATION_DOUBLED[a + jj]
    ba = _PERMUTATION_DOUBLED[b + j]
    bb = _PERMUTATION_DOUBLED[b + jj]

    top = _lerp(
        fx,
        _gradient(_PERMUTATION_DOUBLED[aa], x, y),
        _gradient(_PERMUTATION_DOUBLED[ba], x - 1, y),
    )
    bottom = _lerp(
        fx,
        _gradient(_PERMUTATION_DOUBLED[ab], x, y - 1),
        _gradient(_PERMUTATION_DOUBLED[bb], x - 1, y - 1),
    )
    return _lerp(fy, top, bottom)


def _gradient(hash_value, x, y):
    h = hash_value & 15
    return x * _GRADIENT_X[h] + y * _GRADIENT_Y[h]


def _lerp(t, a, b):
    return a + t * (b - a)


def _scale_request_positions(uv, left, top, right, bottom):
    x_interpolation = linear_interpolation(left, right)
    y_interpolation = linear_interpolation(top, bottom)
    result = uv.copy()
    result[:, 0] = x_interpolation(uv[:, 0])
    result[:, 1] = y_interpolation(uv[:, 1])
    return result
