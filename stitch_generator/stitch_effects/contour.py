from functools import partial

import numpy as np

from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import inverse
from stitch_generator.functions.functions_2d import line
from stitch_generator.functions.get_boundaries import get_boundaries
from stitch_generator.functions.path import Path
from stitch_generator.sampling.samples import samples_by_length


def contour(stitch_length: float):
    return partial(contour_along, stitch_length=stitch_length)


def contour_along(path: Path, stitch_length: float):
    left, right = get_boundaries(path)
    return contour_between(left, right, stitch_length=stitch_length, length=estimate_length(path.position))


def contour_between(boundary_left, boundary_right, stitch_length: float, length: float):
    t = samples_by_length(total_length=length, segment_length=stitch_length, include_endpoint=False)

    start_width = np.linalg.norm(boundary_left(0) - boundary_right(0), axis=1)
    end_width = np.linalg.norm(boundary_left(1) - boundary_right(1), axis=1)
    t_start = samples_by_length(start_width.item(), stitch_length, include_endpoint=True)
    t_end = samples_by_length(end_width.item(), stitch_length, include_endpoint=False)

    boundary_right = inverse(boundary_right)
    connect_end = line(origin=boundary_left(1)[0], to=boundary_right(0)[0])
    connect_start = line(origin=boundary_right(1)[0], to=boundary_left(0)[0])

    stitches = [boundary_left(t)]
    if end_width > 0.5:
        stitches.append(connect_end(t_end))
    stitches.append(boundary_right(t))
    if start_width > 0.5:
        stitches.append(connect_start(t_start))

    stitches = np.concatenate(stitches)

    return stitches
