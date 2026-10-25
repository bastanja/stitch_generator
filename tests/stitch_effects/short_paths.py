from itertools import product

import numpy as np

from stitch_generator.framework import Path
from stitch_generator.functions.function_modifiers import compose
from stitch_generator.functions.functions_1d import arc, constant, linear_interpolation
from stitch_generator.shapes.bezier import bezier
from stitch_generator.shapes.line import line


def line_path(length, width) -> Path:
    return Path(
        *line(origin=(0, 0), to=(length, 0)),
        width=constant(width),
        stroke_alignment=constant(0.5),
    )


short_paths = {
    f"line_{length}_width_{width}": line_path(length, width)
    for length, width in product((0, 1e-6, 0.01, 0.1, 0.5, 1, 2), (0, 0.5, 6))
}
# short curved path with a width of zero at the start and end
short_paths["bezier"] = Path(
    *bezier(control_points=((0, 0), (0.5, 0.5), (1, 0))),
    width=compose(arc, linear_interpolation(0, 2)),
    stroke_alignment=constant(0.5),
)


def assert_at_least_two_stitches(stitches):
    # a stitch effect returns at least a start and an end point
    assert stitches.ndim == 2
    assert stitches.shape[1] == 2
    assert len(stitches) >= 2
    assert np.all(np.isfinite(stitches))
