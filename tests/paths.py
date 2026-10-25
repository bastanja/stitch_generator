from stitch_generator.framework import Path
from stitch_generator.functions.function_modifiers import compose
from stitch_generator.functions.functions_1d import arc, constant, linear_interpolation
from stitch_generator.shapes.bezier import bezier
from stitch_generator.shapes.line import line


def line_path(origin, to, width=1) -> Path:
    shape, direction = line(origin, to)
    return Path(
        shape=shape,
        direction=direction,
        width=constant(width),
        stroke_alignment=constant(0.5),
    )


def bezier_path(control_points, width=1) -> Path:
    shape, direction = bezier(control_points)
    return Path(
        shape=shape,
        direction=direction,
        width=constant(width),
        stroke_alignment=constant(0.5),
    )


def tapered_bezier_path(control_points, max_width) -> Path:
    # the width is zero at the start and end
    shape, direction = bezier(control_points)
    return Path(
        shape=shape,
        direction=direction,
        width=compose(arc, linear_interpolation(0, max_width)),
        stroke_alignment=constant(0.5),
    )
