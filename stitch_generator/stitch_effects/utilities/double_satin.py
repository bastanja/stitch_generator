import numpy as np

from stitch_generator.path.get_boundaries import get_boundaries
from stitch_generator.path.path import Path
from stitch_generator.stitch_effects.utilities.zigzag import double_zigzag_between
from stitch_generator.utilities.types import ConnectFunction, Function2D, SamplingFunction, Array2D


def double_satin_along(path: Path, sampling_function: SamplingFunction, connect_function: ConnectFunction) -> Array2D:
    return double_satin_between(*get_boundaries(path), sampling_function=sampling_function,
                                connect_function=connect_function, length=path.length)


def double_satin_between(boundary_left: Function2D, boundary_right: Function2D, sampling_function: SamplingFunction,
                         connect_function: ConnectFunction, length: float) -> Array2D:
    points = double_zigzag_between(boundary_left, boundary_right, sampling_function, length)
    connection = [connect_function(*p) for p in zip(points, points[1:])]
    if not np.allclose(connection[-1][-1], points[0]):
        connection.append([points[0]])
    return np.concatenate(connection)
