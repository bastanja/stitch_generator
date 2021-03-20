import numpy as np

from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import inverse
from stitch_generator.path.get_boundaries import get_boundaries
from stitch_generator.path.path import Path
from stitch_generator.sampling.sample_by_length import sample_by_length
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.stitch_effect import StitchEffect
from stitch_generator.utilities.types import Array2D


def contour(stitch_length: float) -> StitchEffect:
    return lambda path: contour_along(path, stitch_length=stitch_length)


def contour_along(path: Path, stitch_length: float) -> Array2D:
    left, right = get_boundaries(path)
    return contour_between(left, right, stitch_length=stitch_length, length=estimate_length(path.position))


def contour_between(boundary_left, boundary_right, stitch_length: float, length: float) -> Array2D:
    t = sample_by_length(total_length=length, segment_length=stitch_length, include_endpoint=False)

    start_width = np.linalg.norm(boundary_left(0) - boundary_right(0), axis=1)
    end_width = np.linalg.norm(boundary_left(1) - boundary_right(1), axis=1)
    t_start = sample_by_length(start_width.item(), stitch_length, include_endpoint=True)
    t_end = sample_by_length(end_width.item(), stitch_length, include_endpoint=False)

    boundary_right = inverse(boundary_right)
    connect_end = line(origin=boundary_left(1)[0], to=boundary_right(0)[0])
    connect_start = line(origin=boundary_right(1)[0], to=boundary_left(0)[0])

    # left boundary
    stitches = [boundary_left(t)]
    # close end
    if not np.isclose(end_width, 0):
        stitches.append(connect_end(t_end))
    # right boundary
    stitches.append(boundary_right(t))
    # close start
    stitches.append(connect_start(t_start))

    stitches = np.concatenate(stitches)

    return stitches
