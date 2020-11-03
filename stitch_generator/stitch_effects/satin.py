import numpy as np

from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.get_boundaries import get_boundaries
from stitch_generator.functions.path import Path
from stitch_generator.functions.sampling import fixed_sampling_with_offset
from stitch_generator.functions.types import ConnectFunction, Function2D
from stitch_generator.stitch_effects.zigzag import zigzag


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

    points = zigzag(boundary_left, boundary_right, sampling_function, length)
    connection = [connect_function(points[i - 1], points[i]) for i in range(1, len(points))]
    return np.concatenate(connection)
