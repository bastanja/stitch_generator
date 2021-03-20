import numpy as np

from stitch_generator.path.get_boundaries import get_boundaries
from stitch_generator.path.path import Path
from stitch_generator.stitch_effects.stitch_effect import StitchEffect
from stitch_generator.stitch_effects.zigzag import zigzag_between
from stitch_generator.utilities.types import Array2D
from stitch_generator.utilities.types import ConnectFunction, Function2D, SamplingFunction


def satin(sampling_function: SamplingFunction, connect_function: ConnectFunction) -> StitchEffect:
    return lambda path: satin_along(path=path, sampling_function=sampling_function, connect_function=connect_function,
                                    length=path.length)


def satin_along(path: Path, sampling_function: SamplingFunction, connect_function: ConnectFunction,
                length: float) -> Array2D:
    return satin_between(*get_boundaries(path), sampling_function=sampling_function, connect_function=connect_function,
                         length=length)


def satin_between(boundary_left: Function2D, boundary_right: Function2D, sampling_function: SamplingFunction,
                  connect_function: ConnectFunction, length: float) -> Array2D:
    points = zigzag_between(boundary_left, boundary_right, sampling_function, length)
    connection = [connect_function(points[i - 1], points[i]) for i in range(1, len(points))]
    return np.concatenate(connection)
