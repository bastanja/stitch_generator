from functools import partial

import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.functions.function_modifiers import inverse
from stitch_generator.functions.get_boundaries import get_boundaries
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.utilities.running_stitch import running_stitch_shape
from stitch_generator.utilities.types import Array2D


def contour_along(path: Path, stitch_length: float) -> Array2D:
    left, right = get_boundaries(path)
    return contour_between(left, right, stitch_length=stitch_length)


def contour_between(boundary_left, boundary_right, stitch_length: float) -> Array2D:
    running_stitch = partial(running_stitch_shape, stitch_length=stitch_length, include_endpoint=False)

    left_0, right_0 = boundary_left(0), boundary_right(0)
    left_1, right_1 = boundary_left(1), boundary_right(1)

    # four sides of the contour
    shapes = [boundary_left,
              line(left_1, right_1) if not np.allclose(left_1, right_1) else None,
              inverse(boundary_right),
              line(right_0, left_0) if not np.allclose(left_0, right_0) else None]

    # collect stitches for all four sides
    stitches = [running_stitch(shape) for shape in shapes if shape is not None]

    # add end point if it is not the same as the start point
    if not np.all(np.isclose(left_0, stitches[-1][-1])):
        stitches.append(left_0)

    return np.concatenate(stitches)
