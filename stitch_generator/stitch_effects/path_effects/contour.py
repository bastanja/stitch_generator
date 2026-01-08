from functools import partial

import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import Coordinates
from stitch_generator.functions.function_modifiers import inverse
from stitch_generator.helpers.path_operations import get_boundaries
from stitch_generator.shapes.line import line_shape
from ..shape_effects.running_stitch import (
    running_stitch_on_shape,
)


def contour(stitch_length: float) -> StitchEffect:
    """Creates a contour stitch effect.

    A running stitch line along the left and right boundary of the Path, closed at both ends.

    Args:
        stitch_length: The length of each stitch segment.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.

    Example:
        ```python
        from stitch_generator.stitch_effects.path_effects.contour import contour

        effect = contour(stitch_length=3)
        stitches = effect(path)
        ```
    """
    return lambda path: contour_along(path, stitch_length=stitch_length)


def contour_along(path: Path, stitch_length: float) -> Coordinates:
    """Creates a countour along the left and right boundary of the Path, closed at both ends.

    Args:
        path: The path to create contour stitches along.
        stitch_length: The length of each stitch segment.

    Returns:
        Coordinates representing the contour stitches.
    """
    left, right = get_boundaries(path)
    return contour_between(left, right, stitch_length=stitch_length)


def contour_between(boundary_left, boundary_right, stitch_length: float) -> Coordinates:
    """Creates a contour along two boundaries, closed at both ends.

    Contour goes along the left boundary, connects the end of the left to the end of the right
    boundary, backwards along the right boundary and back to the start of the left boundary.

    Args:
        boundary_left: Function representing the left boundary of the path.
        boundary_right: Function representing the right boundary of the path.
        stitch_length: The length of each stitch segment.

    Returns:
        Coordinates representing the contour stitches connecting the boundaries.
    """
    running_stitch = partial[Coordinates](
        running_stitch_on_shape, stitch_length=stitch_length, include_endpoint=False
    )

    left_0, right_0 = boundary_left(0), boundary_right(0)
    left_1, right_1 = boundary_left(1), boundary_right(1)

    # four sides of the contour
    shapes = [
        boundary_left,
        line_shape(left_1, right_1) if not np.allclose(left_1, right_1) else None,
        inverse(boundary_right),
        line_shape(right_0, left_0) if not np.allclose(left_0, right_0) else None,
    ]

    # collect stitches for all four sides
    stitches = [running_stitch(shape) for shape in shapes if shape is not None]

    # add end point if it is not the same as the start point
    if not np.all(np.isclose(left_0, stitches[-1][-1])):
        stitches.append(left_0)

    return np.concatenate(stitches)
