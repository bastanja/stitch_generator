from typing import Sequence, Tuple

from stitch_generator.framework.types import Function2D
from stitch_generator.functions.function_modifiers import repeat, mix
from stitch_generator.functions.functions_1d import linear_interpolation
from stitch_generator.shapes.circle import circle_shape, circle_direction


def spiral(inner_radius: float, outer_radius: float, turns: float, center: Sequence[float] = (0, 0)) \
        -> Tuple[Function2D, Function2D]:
    shape = spiral_shape(inner_radius=inner_radius, outer_radius=outer_radius, turns=turns, center=center)
    direction = spiral_direction(turns=turns)
    return shape, direction


def spiral_shape(inner_radius: float, outer_radius: float, turns: float,
                 center: Sequence[float] = (0, 0)) -> Function2D:
    inner_circle = repeat(turns, circle_shape(inner_radius, center=center))
    outer_circle = repeat(turns, circle_shape(outer_radius, center=center))
    shape = mix(inner_circle, outer_circle, linear_interpolation(0, 1))
    return shape


def spiral_direction(turns: float):
    return repeat(turns, circle_direction)
