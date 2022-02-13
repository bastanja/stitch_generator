import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import ConnectFunction, SamplingFunction
from stitch_generator.framework.types import Function2D, Array2D
from stitch_generator.functions.get_boundaries import get_boundaries
from stitch_generator.stitch_effects.path_effects.zigzag import double_zigzag_between


def double_satin(sampling_function: SamplingFunction, connect_function: ConnectFunction) -> StitchEffect:
    return lambda path: double_satin_along(path=path, sampling_function=sampling_function,
                                           connect_function=connect_function)


def double_satin_along(path: Path, sampling_function: SamplingFunction, connect_function: ConnectFunction) -> Array2D:
    return double_satin_between(*get_boundaries(path), sampling_function=sampling_function,
                                connect_function=connect_function, length=path.length)


def double_satin_between(boundary_left: Function2D, boundary_right: Function2D, sampling_function: SamplingFunction,
                         connect_function: ConnectFunction, length: float) -> Array2D:
    points = double_zigzag_between(boundary_left, boundary_right, sampling_function, length)
    connection = [connect_function(*p) for p in zip(points, np.roll(points, -1, 0))]
    return np.concatenate(connection)
