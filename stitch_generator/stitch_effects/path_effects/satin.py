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
    return _connect_points(points, line_subdivision)


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
    # double_zigzag_between already ends at its start point
    return _connect_points(points, line_subdivision)


def _connect_points(points, line_subdivision: SubdivisionFunction) -> Array2D:
    # each line leaves out its end point, as it is the start point of the next line
    line_subdivision = remove_end(line_subdivision)
    connection = [subdivide_line(*p, line_subdivision) for p in zip(points, points[1:])]
    return np.concatenate(connection + [points[-1:]])
