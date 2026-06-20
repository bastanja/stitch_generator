import numpy as np

from stitch_generator.framework import Path
from stitch_generator.framework import StitchEffect
from stitch_generator.framework import Array2D
from stitch_generator.framework import Function2D, SubdivisionFunction
from stitch_generator.functions import estimate_length
from stitch_generator.helpers import get_boundaries
from ..path_effects.zigzag import (
    zigzag_between,
    double_zigzag_between,
)
from stitch_generator.helpers import subdivide_line
from stitch_generator.subdivision import regular


def satin(
    spacing_function: SubdivisionFunction, line_subdivision: SubdivisionFunction
) -> StitchEffect:
    return lambda path: satin_along(
        path=path, spacing_function=spacing_function, line_subdivision=line_subdivision
    )


def simple_satin(spacing: float, stitch_length: float) -> StitchEffect:
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
    points = zigzag_between(boundary_left, boundary_right, spacing_function, length)
    connection = [subdivide_line(*p, line_subdivision) for p in zip(points, points[1:])]
    connection = connection + [[points[-1]]]
    return np.concatenate(connection)


def double_satin(
    spacing_function: SubdivisionFunction, line_subdivision: SubdivisionFunction
) -> StitchEffect:
    return lambda path: double_satin_along(
        path=path, spacing_function=spacing_function, line_subdivision=line_subdivision
    )


def double_satin_along(
    path: Path,
    spacing_function: SubdivisionFunction,
    line_subdivision: SubdivisionFunction,
) -> Array2D:
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
    points = double_zigzag_between(
        boundary_left, boundary_right, spacing_function, length
    )
    connection = [
        subdivide_line(*p, line_subdivision)
        for p in zip(points, np.roll(points, -1, 0))
    ]
    return np.concatenate(connection)
