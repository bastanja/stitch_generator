from typing import Sequence

from stitch_generator.functions.function_modifiers import repeat, mix
from stitch_generator.functions.functions_1d import linear_interpolation
from stitch_generator.shapes.circle import circle
from stitch_generator.framework.types import Function2D


def spiral(inner_radius: float, outer_radius: float, turns: float, center: Sequence[float] = (0, 0)) -> Function2D:
    inner_circle = repeat(turns, circle(inner_radius, center=center))
    outer_circle = repeat(turns, circle(outer_radius, center=center))
    return mix(inner_circle, outer_circle, linear_interpolation(0, 1))
