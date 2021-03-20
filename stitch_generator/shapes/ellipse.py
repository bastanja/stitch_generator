from typing import Sequence

from stitch_generator.functions.function_modifiers import scale, add
from stitch_generator.functions.functions_1d import cosinus, sinus, constant
from stitch_generator.functions.functions_2d import function_2d
from stitch_generator.utilities.types import Function2D


def ellipse(rx: float, ry: float, center: Sequence[float] = (0, 0)) -> Function2D:
    fx = cosinus()
    fy = sinus()
    fx = scale(rx, fx)
    fy = scale(ry, fy)
    f = function_2d(fx, fy)
    if center != (0, 0):
        c = function_2d(constant(center[0]), constant(center[1]))
        f = add(f, c)
    return f
