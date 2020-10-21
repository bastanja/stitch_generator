import numpy as np

from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.get_boundaries import get_boundaries
from stitch_generator.functions.path import Path
from stitch_generator.functions.sampling import fixed_sampling_with_offset, regular_sampling
from stitch_generator.functions.types import ConnectFunction, SamplingFunction, Function2D


def satin(stitch_spacing, connect_function: ConnectFunction):
    return lambda path: satin_along(path=path, stitch_spacing=stitch_spacing, connect_function=connect_function,
                                    length=estimate_length(path.position))


def satin_along(path: Path, stitch_spacing: float, connect_function: ConnectFunction, length: float):
    return satin_between(*get_boundaries(path), stitch_spacing=stitch_spacing, connect_function=connect_function,
                         length=length)


def satin_between(boundary_left: Function2D, boundary_right: Function2D, stitch_spacing: float,
                  connect_function: ConnectFunction, length: float):
    sampling_function = fixed_sampling_with_offset(stitch_length=stitch_spacing, alignment=0, offset=0,
                                                   include_endpoint=True)

    points = _satin(boundary_left, boundary_right, sampling_function, length)
    connection = [connect_function(points[i - 1], points[i]) for i in range(1, len(points))]
    return np.concatenate(connection)


def double_satin(stitch_spacing: float, connect_function: ConnectFunction):
    return lambda path: double_satin_along(path=path, stitch_spacing=stitch_spacing, connect_function=connect_function,
                                           length=estimate_length(path.position))


def double_satin_along(path: Path, stitch_spacing: float, connect_function: ConnectFunction, length: float):
    return double_satin_between(*get_boundaries(path), stitch_spacing=stitch_spacing, connect_function=connect_function,
                                length=length)


def double_satin_between(boundary_left: Function2D, boundary_right: Function2D, stitch_spacing: float,
                         connect_function: ConnectFunction, length: float):
    sampling_function = regular_sampling(stitch_length=stitch_spacing, include_endpoint=True)

    points_forward = _satin(boundary_left, boundary_right, sampling_function, length)
    points_backward = _satin(boundary_right, boundary_left, sampling_function, length)
    points_backward = np.flipud(points_backward)

    if np.allclose(points_forward[-1], points_backward[0]):
        points_backward = points_backward[1:]

    all_points = np.concatenate((points_forward, points_backward, [points_forward[0]]))
    connection = [connect_function(*p) for p in zip(all_points, all_points[1:])]

    return np.concatenate(connection)


def _satin(boundary_left: Function2D, boundary_right: Function2D, sampling_function: SamplingFunction, length: float):
    p = sampling_function(length)
    if len(p) < 2:
        p = np.array([0, 1], dtype=float)
    stitches = np.zeros((len(p), 2))
    stitches[0::2] = boundary_left(p[0::2])
    stitches[1::2] = boundary_right(p[1::2])
    return stitches
