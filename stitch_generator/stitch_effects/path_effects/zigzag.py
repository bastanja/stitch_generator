import numpy as np

from stitch_generator.framework import (
    Coordinates,
    Function2D,
    Path,
    StitchEffect,
    SubdivisionFunction,
)
from stitch_generator.functions import estimate_length
from stitch_generator.helpers import get_boundaries
from stitch_generator.subdivision import regular


def zigzag(spacing_function: SubdivisionFunction) -> StitchEffect:
    """Creates a zigzag stitch effect.

    A simple zigzag line between the left and right boundary of the path. In contrast to satin,
    it has no intermediate stitches.

    Args:
        spacing_function: Function that subdivides the path length to determine spacing
            between zigzag points.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.

    Example:
        ```python
        from stitch_generator.subdivision import regular
        from stitch_generator.stitch_effects.path_effects import zigzag

        effect = zigzag(spacing_function=regular(3))
        stitches = effect(path)
        ```

    Note:
        zigzag has no intermediate stitches. Therefore, it may produce very long stitches which
        are not possible to use with an embroidery machine. Take care to keep the paths narrow
        enough for zigzag stitches.
    """
    return lambda path: zigzag_along(path=path, spacing_function=spacing_function)


def simple_zigzag(spacing: float) -> StitchEffect:
    """Creates a simple zigzag stitch effect with regular spacing.

    Args:
        spacing: The spacing between zigzag points.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.
    """
    return lambda path: zigzag_along(path=path, spacing_function=regular(spacing))


def zigzag_along(path: Path, spacing_function: SubdivisionFunction) -> Coordinates:
    """Creates zigzag stitches along a path.

    Args:
        path: The path to create zigzag stitches along.
        spacing_function: Function that subdivides the path length to determine spacing
            between zigzag points.

    Returns:
        Coordinates representing the zigzag stitches.
    """
    path_length = estimate_length(path.shape)
    return zigzag_between(
        *get_boundaries(path), spacing_function=spacing_function, length=path_length
    )


def zigzag_between(
    boundary_left: Function2D,
    boundary_right: Function2D,
    spacing_function: SubdivisionFunction,
    length: float,
) -> Coordinates:
    """Creates zigzag stitches between two boundaries.

    Args:
        boundary_left: Function representing the left boundary of the path.
        boundary_right: Function representing the right boundary of the path.
        spacing_function: Function that subdivides the path length to determine spacing
            between zigzag points.
        length: The length of the path.

    Returns:
        Coordinates representing the zigzag stitches.
    """
    p = spacing_function(length)
    if len(p) < 2:
        p = boundary_left(0)
    stitches = boundary_left(p)
    stitches[1::2] = boundary_right(p[1::2])
    return stitches


def double_zigzag(spacing_function: SubdivisionFunction) -> StitchEffect:
    """Creates a double zigzag stitch effect.

    Similar to zigzag, but creates two overlapping zigzag patterns.

    Args:
        spacing_function: Function that subdivides the path length to determine spacing
            between zigzag points.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.

    Example:
        ```python
        from stitch_generator.subdivision import regular
        from stitch_generator.stitch_effects.path_effects import double_zigzag

        effect = double_zigzag(spacing_function=regular(3))
        stitches = effect(path)
        ```

    Note:
        double_zigzag has no intermediate stitches. Therefore, it may produce very long
        stitches which are not possible to use with an embroidery machine. Take care to
        keep the paths narrow enough for zigzag stitches.
    """
    return lambda path: double_zigzag_along(
        path=path, spacing_function=spacing_function
    )


def double_zigzag_along(
    path: Path, spacing_function: SubdivisionFunction
) -> Coordinates:
    """Creates double zigzag stitches along a path.

    Args:
        path: The path to create double zigzag stitches along.
        spacing_function: Function that subdivides the path length to determine spacing
            between zigzag points.

    Returns:
        Coordinates representing the double zigzag stitches.
    """
    path_length = estimate_length(path.shape)
    return double_zigzag_between(
        *get_boundaries(path), spacing_function=spacing_function, length=path_length
    )


def double_zigzag_between(
    boundary_left: Function2D,
    boundary_right: Function2D,
    spacing_function: SubdivisionFunction,
    length: float,
) -> Coordinates:
    """Creates double zigzag stitches between two boundaries.

    Args:
        boundary_left: Function representing the left boundary of the path.
        boundary_right: Function representing the right boundary of the path.
        spacing_function: Function that subdivides the path length to determine spacing
            between zigzag points.
        length: The length of the path.

    Returns:
        Coordinates representing the double zigzag stitches.
    """
    points_forward = zigzag_between(
        boundary_left, boundary_right, spacing_function, length
    )
    points_backward = zigzag_between(
        boundary_right, boundary_left, spacing_function, length
    )

    if np.allclose(points_forward[-1], points_backward[-1]):
        points_backward = points_backward[:-1]

    if np.allclose(points_forward[0], points_backward[0]):
        points_backward = points_backward[1:]

    return np.concatenate(
        (points_forward, np.flipud(points_backward), [points_forward[0]])
    )
