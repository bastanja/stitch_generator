import numpy as np

from stitch_generator.framework.path import Path, get_boundaries
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import Function2D, SubdivisionFunction, Array2D
from stitch_generator.subdivision.subdivide_by_length import regular


def zigzag(spacing_function: SubdivisionFunction) -> StitchEffect:
    return lambda path: zigzag_along(path=path, spacing_function=spacing_function)


def simple_zigzag(spacing: float):
    return lambda path: zigzag_along(path=path, spacing_function=regular(spacing))


def zigzag_along(path: Path, spacing_function: SubdivisionFunction) -> Array2D:
    return zigzag_between(*get_boundaries(path), spacing_function=spacing_function, length=path.length)


def zigzag_between(boundary_left: Function2D, boundary_right: Function2D, spacing_function: SubdivisionFunction,
                   length: float) -> Array2D:
    p = spacing_function(length)
    if len(p) < 2:
        p = boundary_left(0)
    stitches = boundary_left(p)
    stitches[1::2] = boundary_right(p[1::2])
    return stitches


def double_zigzag(spacing_function: SubdivisionFunction) -> StitchEffect:
    return lambda path: double_zigzag_along(path=path, spacing_function=spacing_function)


def double_zigzag_along(path: Path, spacing_function: SubdivisionFunction) -> Array2D:
    return double_zigzag_between(*get_boundaries(path), spacing_function=spacing_function, length=path.length)


def double_zigzag_between(boundary_left: Function2D, boundary_right: Function2D, spacing_function: SubdivisionFunction,
                          length: float) -> Array2D:
    points_forward = zigzag_between(boundary_left, boundary_right, spacing_function, length)
    points_backward = zigzag_between(boundary_right, boundary_left, spacing_function, length)

    if np.allclose(points_forward[-1], points_backward[-1]):
        points_backward = points_backward[:-1]

    if np.allclose(points_forward[0], points_backward[0]):
        points_backward = points_backward[1:]

    return np.concatenate((points_forward, np.flipud(points_backward), [points_forward[0]]))
