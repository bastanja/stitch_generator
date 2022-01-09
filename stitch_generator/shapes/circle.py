from typing import Sequence

from stitch_generator.shapes.ellipse import ellipse
from stitch_generator.framework.types import Function2D


def circle(radius: float = 1, center: Sequence[float] = (0, 0)) -> Function2D:
    return ellipse(rx=radius, ry=radius, center=center)
