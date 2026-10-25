import numpy as np

from stitch_generator.framework import Path
from stitch_generator.functions.functions_1d import constant
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.shape_effects.variable_running_stitch import (
    variable_running_stitch,
)


def line_path(origin, to) -> Path:
    shape, direction = line(origin, to)
    return Path(
        shape=shape,
        direction=direction,
        width=constant(1),
        stroke_alignment=constant(0.5),
    )


def do_test(width):
    effect = variable_running_stitch(
        stitch_length=3,
        width_profile=constant(width),
        min_strokes=1,
        max_strokes=5,
        stroke_spacing=0.3,
    )
    return effect(line_path(origin=(0, 0), to=(30, 0)))


def test_variable_running_stitch_clamps_width_profile():
    # widths outside [0, 1] behave like the nearest valid width
    assert np.allclose(do_test(width=2), do_test(width=1))
    assert np.allclose(do_test(width=-1), do_test(width=0))
