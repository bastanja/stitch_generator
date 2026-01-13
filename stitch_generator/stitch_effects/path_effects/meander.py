import numpy as np

from stitch_generator.framework import Path
from stitch_generator.framework import StitchEffect
from stitch_generator.framework import (
    Coordinates,
    SubdivisionFunction,
    CoordinateFunction,
)
from stitch_generator.functions import ensure_2d_shape
from stitch_generator.functions import estimate_length
from stitch_generator.helpers import get_boundaries
from stitch_generator.helpers import subdivide_line
from stitch_generator.subdivision import regular


def meander(
    spacing_function: SubdivisionFunction,
    line_subdivision: SubdivisionFunction,
    join_ends: bool = False,
) -> StitchEffect:
    """Creates a meander stitch effect.

    A line that meanders back and forth between the left and right boundary of the Path.

    Args:
        spacing_function: Function that subdivides the path length to determine spacing
            between meander lines.
        line_subdivision: Function that subdivides each meander line to create stitches.
        join_ends: If True, connects the ends of consecutive meander lines. Defaults to False.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.

    Example:
        ```python
        from stitch_generator.subdivision import regular
        from stitch_generator.stitch_effects.path_effects import meander

        effect = meander(spacing_function=regular(3), line_subdivision=regular(3))
        stitches = effect(path)
        ```
    """
    return lambda path: meander_along(
        path=path,
        spacing_function=spacing_function,
        line_subdivision=line_subdivision,
        join_ends=join_ends,
    )


def simple_meander(spacing: float, stitch_length: float) -> StitchEffect:
    """Creates a simple meander stitch effect with regular spacing.

    Args:
        spacing: The spacing between meander lines.
        stitch_length: The length of each stitch segment.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.
    """
    return lambda path: meander_along(
        path=path,
        spacing_function=regular(spacing),
        line_subdivision=regular(stitch_length),
        join_ends=False,
    )


def meander_along(
    path: Path,
    spacing_function: SubdivisionFunction,
    line_subdivision: SubdivisionFunction,
    join_ends: bool = False,
) -> Coordinates:
    """Creates meander stitches along a path.

    Args:
        path: The path to create meander stitches along.
        spacing_function: Function that subdivides the path length to determine spacing
            between meander lines.
        line_subdivision: Function that subdivides each meander line to create stitches.
        join_ends: If True, connects the ends of consecutive meander lines. Defaults to False.

    Returns:
        Coordinates representing the meander stitches.
    """
    path_length = estimate_length(path.shape)
    return meander_between(
        *get_boundaries(path),
        spacing_function=spacing_function,
        line_subdivision=line_subdivision,
        join_ends=join_ends,
        length=path_length,
    )


def meander_between(
    boundary_left,
    boundary_right,
    spacing_function: SubdivisionFunction,
    line_subdivision: SubdivisionFunction,
    length: float,
    join_ends: bool = False,
) -> Coordinates:
    """Creates meander stitches between two boundaries.
    Args:
        boundary_left: Function representing the left boundary of the path.
        boundary_right: Function representing the right boundary of the path.
        spacing_function: Function that subdivides the path length to determine spacing
            between meander lines.
        line_subdivision: Function that subdivides each meander line to create stitches.
        length: The length of the path.
        join_ends: If True, connects the ends of consecutive meander lines. Defaults to False.
    Returns:
        Coordinates representing the meander stitches.
    """
    points = _meander(
        boundary_left, boundary_right, spacing_function=spacing_function, length=length
    )

    parts = [
        subdivide_line(points[i - 1], points[i], line_subdivision)
        for i in range(1, len(points), 2)
    ]

    return _connect_parts(parts, join_ends)


def _connect_parts(parts, join_ends: bool):
    """Connects meander line parts together.

    Args:
        parts: List of coordinate arrays representing meander line segments.
        join_ends: If True, connects the ends of consecutive parts. Defaults to False.

    Returns:
        Concatenated coordinates with optional end connections.
    """
    if not join_ends:
        return np.concatenate(parts)

    last_point = None

    def modify_part(part):
        if len(part) == 0:
            return part

        nonlocal last_point

        try:
            part[0] = (part[0] + last_point) / 2
        except TypeError:
            # if last_point was not set yet, ignore it
            pass

        last_point = part[-1]
        return part[:-1]

    return np.concatenate(
        [modify_part(p) for p in parts] + [ensure_2d_shape(last_point)]
    )


def _meander(
    boundary_left: CoordinateFunction,
    boundary_right: CoordinateFunction,
    spacing_function: SubdivisionFunction,
    length: float,
) -> Coordinates:
    """Generates the basic meander pattern coordinates.

    Args:
        boundary_left: Function representing the left boundary of the path.
        boundary_right: Function representing the right boundary of the path.
        spacing_function: Function that subdivides the path length to determine spacing.
        length: The length of the path.

    Returns:
        Stitch coordinates forming the meander pattern.
    """
    t = spacing_function(length)

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
