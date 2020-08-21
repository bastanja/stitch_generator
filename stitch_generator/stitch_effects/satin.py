import numpy as np

from stitch_generator.functions.get_boundaries import get_boundaries
from stitch_generator.functions.path import Path
from stitch_generator.functions.samples import samples_by_fixed_length


def satin_along(path: Path, stitch_spacing, connect_function, length):
    return satin_between(*get_boundaries(path), stitch_spacing, connect_function, length)


def satin_between(boundary_left, boundary_right, stitch_spacing, connect_function, length):
    points = _satin(boundary_left, boundary_right, stitch_spacing, length)
    connection = [connect_function(points[i - 1], points[i]) for i in range(1, len(points))]
    return np.concatenate(connection)


def _satin(boundary_left, boundary_right, stitch_spacing, length):
    p = samples_by_fixed_length(length, stitch_spacing, include_endpoint=False)
    if len(p) < 2:
        p = np.array([0, 1], dtype=float)
    stitches = np.zeros((len(p), 2))
    stitches[0::2] = boundary_left(p[0::2])
    stitches[1::2] = boundary_right(p[1::2])
    return stitches
