from typing import Sequence, Tuple

from stitch_generator.framework import Function2D
from stitch_generator.functions import cosinus, function_2d, sinus

from .ellipse import ellipse_shape


def circle(
    radius: float = 1, center: Sequence[float] = (0, 0)
) -> Tuple[Function2D, Function2D]:
    shape = circle_shape(radius=radius, center=center)
    return shape, circle_direction


def circle_shape(radius: float = 1, center: Sequence[float] = (0, 0)) -> Function2D:
    return ellipse_shape(rx=radius, ry=radius, center=center)


circle_direction = function_2d(cosinus, sinus)
