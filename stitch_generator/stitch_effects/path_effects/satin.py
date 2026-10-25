import numpy as np

from stitch_generator.framework import (
    Array2D,
    Function2D,
    Path,
    StitchEffect,
    SubdivisionFunction,
)
from stitch_generator.functions import estimate_length
from stitch_generator.helpers import get_boundaries, subdivide_line
from stitch_generator.subdivision import regular, remove_end

from ..path_effects.zigzag import double_zigzag_between, zigzag_between


def satin(
    spacing_function: SubdivisionFunction, line_subdivision: SubdivisionFunction
) -> StitchEffect:
    """Creates a satin stitch effect.

    A zigzag line between the left and right boundary of the path with intermediate stitches
    based on a subdivision function.

    Args:
        spacing_function: Function that subdivides the path length to determine spacing
            between zigzag points.
        line_subdivision: Function that subdivides each zigzag line to create intermediate
            stitches.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.

    Example:
        ```python
        from stitch_generator.subdivision import regular
        from stitch_generator.stitch_effects.path_effects import satin

        effect = satin(spacing_function=regular(2), line_subdivision=regular(3))
        stitches = effect(path)
        ```
    """
    return lambda path: satin_along(
        path=path, spacing_function=spacing_function, line_subdivision=line_subdivision
    )


def simple_satin(spacing: float, stitch_length: float) -> StitchEffect:
    """Creates a simple satin stitch effect with regular spacing.

    Args:
        spacing: The spacing between zigzag points.
        stitch_length: The length of the intermediate stitches.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.
    """
    return lambda path: satin_along(
        path=path,
        spacing_function=regular(spacing),
        line_subdivision=regular(stitch_length),
    )


def satin_along(
    path: Path,
    spacing_function: SubdivisionFunction,
    line_subdivision: SubdivisionFunction,
) -> Array2D:
    """Creates satin stitches along a path.

    Args:
        path: The path to create satin stitches along.
        spacing_function: Function that subdivides the path length to determine spacing
            between zigzag points.
        line_subdivision: Function that subdivides each zigzag line to create intermediate
            stitches.

    Returns:
        Coordinates representing the satin stitches.
    """
    path_length = estimate_length(path.shape)
    return satin_between(
        *get_boundaries(path),
        spacing_function=spacing_function,
        line_subdivision=line_subdivision,
        length=path_length,
    )


def satin_between(
    boundary_left: Function2D,
    boundary_right: Function2D,
    spacing_function: SubdivisionFunction,
    line_subdivision: SubdivisionFunction,
    length: float,
) -> Array2D:
    """Creates satin stitches between two boundaries.

    Args:
        boundary_left: Function representing the left boundary of the path.
        boundary_right: Function representing the right boundary of the path.
        spacing_function: Function that subdivides the path length to determine spacing
            between zigzag points.
        line_subdivision: Function that subdivides each zigzag line to create intermediate
            stitches.
        length: The length of the path.

    Returns:
        Coordinates representing the satin stitches.
    """
    points = zigzag_between(boundary_left, boundary_right, spacing_function, length)
    return _connect_points(points, line_subdivision)


def double_satin(
    spacing_function: SubdivisionFunction, line_subdivision: SubdivisionFunction
) -> StitchEffect:
    """Creates a double satin stitch effect.

    Similar to satin, but goes back and forth along the path, so that two satin patterns
    overlap and the stitches end where they started.

    Args:
        spacing_function: Function that subdivides the path length to determine spacing
            between zigzag points.
        line_subdivision: Function that subdivides each zigzag line to create intermediate
            stitches.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.

    Example:
        ```python
        from stitch_generator.subdivision import regular
        from stitch_generator.stitch_effects.path_effects import double_satin

        effect = double_satin(spacing_function=regular(3), line_subdivision=regular(3))
        stitches = effect(path)
        ```
    """
    return lambda path: double_satin_along(
        path=path, spacing_function=spacing_function, line_subdivision=line_subdivision
    )


def double_satin_along(
    path: Path,
    spacing_function: SubdivisionFunction,
    line_subdivision: SubdivisionFunction,
) -> Array2D:
    """Creates double satin stitches along a path.

    Args:
        path: The path to create double satin stitches along.
        spacing_function: Function that subdivides the path length to determine spacing
            between zigzag points.
        line_subdivision: Function that subdivides each zigzag line to create intermediate
            stitches.

    Returns:
        Coordinates representing the double satin stitches.
    """
    path_length = estimate_length(path.shape)
    return double_satin_between(
        *get_boundaries(path),
        spacing_function=spacing_function,
        line_subdivision=line_subdivision,
        length=path_length,
    )


def double_satin_between(
    boundary_left: Function2D,
    boundary_right: Function2D,
    spacing_function: SubdivisionFunction,
    line_subdivision: SubdivisionFunction,
    length: float,
) -> Array2D:
    """Creates double satin stitches between two boundaries.

    Args:
        boundary_left: Function representing the left boundary of the path.
        boundary_right: Function representing the right boundary of the path.
        spacing_function: Function that subdivides the path length to determine spacing
            between zigzag points.
        line_subdivision: Function that subdivides each zigzag line to create intermediate
            stitches.
        length: The length of the path.

    Returns:
        Coordinates representing the double satin stitches.
    """
    points = double_zigzag_between(
        boundary_left, boundary_right, spacing_function, length
    )
    # double_zigzag_between already ends at its start point
    return _connect_points(points, line_subdivision)


def _connect_points(points, line_subdivision: SubdivisionFunction) -> Array2D:
    # each line leaves out its end point, as it is the start point of the next line
    line_subdivision = remove_end(line_subdivision)
    connection = [subdivide_line(*p, line_subdivision) for p in zip(points, points[1:])]
    return np.concatenate(connection + [points[-1:]])
