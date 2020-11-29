import numpy as np

from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.path.get_boundaries import get_boundaries
from stitch_generator.path.path import Path
from stitch_generator.stitch_effects.stitch_effect import StitchEffect
from stitch_generator.stitch_effects.zigzag import double_zigzag_between
from stitch_generator.utilities.types import ConnectFunction, Function2D, SamplingFunction, Array2D


def double_satin(sampling_function: SamplingFunction, connect_function: ConnectFunction) -> StitchEffect:
    return lambda path: double_satin_along(path=path, sampling_function=sampling_function,
                                           connect_function=connect_function,
                                           length=estimate_length(path.position))


def double_satin_along(path: Path, sampling_function: SamplingFunction, connect_function: ConnectFunction,
                       length: float) -> Array2D:
    return double_satin_between(*get_boundaries(path), sampling_function=sampling_function,
                                connect_function=connect_function, length=length)


def double_satin_between(boundary_left: Function2D, boundary_right: Function2D, sampling_function: SamplingFunction,
                         connect_function: ConnectFunction, length: float) -> Array2D:
    points = double_zigzag_between(boundary_left, boundary_right, sampling_function, length)
    connection = [connect_function(*p) for p in zip(points, points[1:])]
    if not np.allclose(connection[-1][-1], points[0]):
        connection.append([points[0]])
    return np.concatenate(connection)
