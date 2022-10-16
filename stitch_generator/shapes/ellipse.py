from typing import Sequence, Tuple

from stitch_generator.framework.types import Function2D
from stitch_generator.functions.function_modifiers import scale, add
from stitch_generator.functions.functions_1d import cosinus, sinus, constant
from stitch_generator.functions.functions_2d import function_2d


def ellipse(rx: float, ry: float, center: Sequence[float] = (0, 0)) -> Tuple[Function2D, Function2D]:
    shape = ellipse_shape(rx=rx, ry=ry, center=center)
    direction = ellipse_direction(rx=rx, ry=ry)
    return shape, direction


def ellipse_shape(rx: float, ry: float, center: Sequence[float] = (0, 0)) -> Function2D:
    fx = scale(rx, cosinus)
    fy = scale(ry, sinus)
    shape = function_2d(fx, fy)
    if center != (0, 0):
        c = function_2d(constant(center[0]), constant(center[1]))
        shape = add(shape, c)

    return shape


def ellipse_direction(rx: float, ry: float):
    return function_2d(cosinus, sinus)  # ToDo: should be normalized direction from center to point on ellipse
