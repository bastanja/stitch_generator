from typing import Tuple

from stitch_generator.framework.path import Path
from stitch_generator.functions.function_modifiers import multiply, subtract, add
from stitch_generator.functions.functions_1d import constant
from stitch_generator.utilities.types import Function2D


def get_boundaries(path: Path) -> Tuple[Function2D, Function2D]:
    """
    Calculates the left and right boundary of a path

    Args:
        path: The path for which the boundaries are calculated

    Returns:
        left and right boundary of the path
    """
    positive_width = multiply(path.width, path.stroke_alignment)
    negative_width = multiply(path.width, subtract(constant(1), path.stroke_alignment))

    left = add(path.shape, multiply(path.direction, positive_width))
    right = subtract(path.shape, multiply(path.direction, negative_width))

    return left, right
