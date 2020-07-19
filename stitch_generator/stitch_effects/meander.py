import numpy as np

from stitch_generator.functions.get_boundaries import get_boundaries
from stitch_generator.functions.samples import linspace


def meander_along(f, direction, width, offset, stitch_spacing, connect_function, length):
    return meander_between(*get_boundaries(f, direction, width, offset), stitch_spacing, connect_function, length)


def meander_between(f1, f2, stitch_spacing, connect_function, length):
    points = _meander(f1, f2, stitch_spacing, length)
    connection = [connect_function(points[i - 1], points[i]) for i in range(1, len(points), 2)]
    return np.concatenate(connection)


def _meander(f1, f2, stitch_spacing, length):
    num_parameters = int(round(length / stitch_spacing))
    parameters = linspace(0, 1, num_parameters, include_endpoint=True)
    stitches = np.zeros((len(parameters) * 2, 2))

    stitches[0::4] = f1(parameters[0::2])
    stitches[1::4] = f2(parameters[0::2])
    stitches[2::4] = f2(parameters[1::2])
    stitches[3::4] = f1(parameters[1::2])

    return stitches
