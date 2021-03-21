import numpy as np

from stitch_generator.path.get_boundaries import get_boundaries
from stitch_generator.path.path import Path
from stitch_generator.utilities.types import Array2D
from stitch_generator.utilities.types import ConnectFunction, SamplingFunction


def meander_along(path: Path, sampling_function: SamplingFunction, connect_function) -> Array2D:
    return meander_between(*get_boundaries(path), sampling_function=sampling_function,
                           connect_function=connect_function, length=path.length)


def meander_between(boundary_left, boundary_right, sampling_function: SamplingFunction,
                    connect_function: ConnectFunction, length) -> Array2D:
    points = _meander(boundary_left, boundary_right, sampling_function=sampling_function, length=length)
    connection = [connect_function(points[i - 1], points[i]) for i in range(1, len(points), 2)]

    last = connection[-1]
    if len(last) > 0 and not np.allclose(last[-1], points[-1]):
        connection.append([points[-1]])

    return np.concatenate(connection)


def _meander(boundary_left, boundary_right, sampling_function: SamplingFunction, length):
    t = sampling_function(length)

    values_left_even = boundary_left(t[0::2])
    values_right_even = boundary_right(t[0::2])
    values_right_odd = boundary_right(t[1::2])
    values_left_odd = boundary_left(t[1::2])

    stitches = np.zeros((len(t) * 2, len(values_left_even[0])))

    stitches[0::4] = values_left_even
    stitches[1::4] = values_right_even
    stitches[2::4] = values_right_odd
    stitches[3::4] = values_left_odd

    return stitches
