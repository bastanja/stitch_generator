import numpy as np

from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import inverse
from stitch_generator.functions.functions_2d import line
from stitch_generator.functions.get_boundaries import get_boundaries
from stitch_generator.functions.path import Path
from stitch_generator.functions.samples import samples_by_length


def contour(path: Path, stitch_length: float):
    left, right = get_boundaries(path)
    right = inverse(right)

    length = estimate_length(path.position)
    t = samples_by_length(total_length=length, segment_length=stitch_length, include_endpoint=False)
    t_start = samples_by_length(path.width(0).item(), stitch_length, include_endpoint=True)
    t_end = samples_by_length(path.width(1).item(), stitch_length, include_endpoint=False)

    connect_end = line(origin=left(1)[0], to=right(0)[0])
    connect_start = line(origin=right(1)[0], to=left(0)[0])

    stitches = [left(t), connect_end(t_end), right(t), connect_start(t_start)]

    stitches = np.concatenate(stitches)

    return stitches
