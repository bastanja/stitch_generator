import numpy as np

from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.path.get_boundaries import get_boundaries
from stitch_generator.path.path import Path
from stitch_generator.utilities.types import ConnectFunction, SamplingFunction


def meander(sampling_function: SamplingFunction, connect_function):
    return lambda path: meander_along(path=path, sampling_function=sampling_function, connect_function=connect_function,
                                      length=estimate_length(path.position))


def meander_along(path: Path, sampling_function: SamplingFunction, connect_function, length):
    return meander_between(*get_boundaries(path), sampling_function=sampling_function,
                           connect_function=connect_function, length=length)


def meander_between(boundary_left, boundary_right, sampling_function: SamplingFunction,
                    connect_function: ConnectFunction, length):
    points = _meander(boundary_left, boundary_right, sampling_function=sampling_function, length=length)
    connection = [connect_function(points[i - 1], points[i]) for i in range(1, len(points), 2)]
    return np.concatenate(connection)


def _meander(boundary_left, boundary_right, sampling_function: SamplingFunction, length):
    t = sampling_function(length)
    stitches = np.zeros((len(t) * 2, 2))

    stitches[0::4] = boundary_left(t[0::2])
    stitches[1::4] = boundary_right(t[0::2])
    stitches[2::4] = boundary_right(t[1::2])
    stitches[3::4] = boundary_left(t[1::2])

    return stitches
