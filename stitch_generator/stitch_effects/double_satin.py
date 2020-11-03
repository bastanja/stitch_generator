import numpy as np

from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.get_boundaries import get_boundaries
from stitch_generator.functions.path import Path
from stitch_generator.functions.sampling import regular_sampling
from stitch_generator.functions.types import ConnectFunction, Function2D
from stitch_generator.stitch_effects.zigzag import double_zigzag


def double_satin(stitch_spacing: float, connect_function: ConnectFunction):
    return lambda path: double_satin_along(path=path, stitch_spacing=stitch_spacing, connect_function=connect_function,
                                           length=estimate_length(path.position))


def double_satin_along(path: Path, stitch_spacing: float, connect_function: ConnectFunction, length: float):
    return double_satin_between(*get_boundaries(path), stitch_spacing=stitch_spacing, connect_function=connect_function,
                                length=length)


def double_satin_between(boundary_left: Function2D, boundary_right: Function2D, stitch_spacing: float,
                         connect_function: ConnectFunction, length: float):
    sampling_function = regular_sampling(stitch_length=stitch_spacing, include_endpoint=True)

    points = double_zigzag(boundary_left, boundary_right, sampling_function, length)
    connection = [connect_function(*p) for p in zip(points, points[1:])]
    return np.concatenate(connection)
