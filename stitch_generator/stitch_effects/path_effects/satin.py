import numpy as np

from stitch_generator.framework.path import Path, get_boundaries
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import Array2D
from stitch_generator.framework.types import ConnectFunction, Function2D, SamplingFunction
from stitch_generator.functions.connect_functions import simple_connect
from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.stitch_effects.path_effects.zigzag import zigzag_between


def satin(sampling_function: SamplingFunction, connect_function: ConnectFunction) -> StitchEffect:
    return lambda path: satin_along(path=path, sampling_function=sampling_function, connect_function=connect_function)


def simple_satin(spacing: float) -> StitchEffect:
    return lambda path: satin_along(
        path=path, sampling_function=regular(spacing),
        connect_function=simple_connect)


def satin_along(path: Path, sampling_function: SamplingFunction, connect_function: ConnectFunction) -> Array2D:
    return satin_between(*get_boundaries(path), sampling_function=sampling_function, connect_function=connect_function,
                         length=path.length)


def satin_between(boundary_left: Function2D, boundary_right: Function2D, sampling_function: SamplingFunction,
                  connect_function: ConnectFunction, length: float) -> Array2D:
    points = zigzag_between(boundary_left, boundary_right, sampling_function, length)
    connection = [connect_function(points[i - 1], points[i]) for i in range(1, len(points))]
    return np.concatenate(connection)
