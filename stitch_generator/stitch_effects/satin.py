import numpy as np

from stitch_generator.functions.get_boundaries import get_boundaries
from stitch_generator.functions.samples import samples_by_fixed_length


def satin_along(f, direction, width, offset, stitch_spacing, connect_function, length):
    return satin_between(*get_boundaries(f, direction, width, offset), stitch_spacing, connect_function, length)


def satin_between(f1, f2, stitch_spacing, connect_function, length):
    points = _satin(f1, f2, stitch_spacing, length)
    connection = [connect_function(points[i - 1], points[i]) for i in range(1, len(points))]
    return np.concatenate(connection)


def _satin(f1, f2, stitch_spacing, length):
    p = samples_by_fixed_length(length, stitch_spacing, include_endpoint=False)
    if len(p) < 2:
        p = np.array([0, 1], dtype=float)
    stitches = np.zeros((len(p), 2))
    stitches[0::2] = f1(p[0::2])
    stitches[1::2] = f2(p[1::2])
    return stitches
