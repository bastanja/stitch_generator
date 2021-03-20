from typing import Tuple

from stitch_generator.functions.function_modifiers import multiply, subtract, add, maximum, minimum, repeat, shift
from stitch_generator.functions.functions_1d import constant
from stitch_generator.path.path import Path
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

    left = add(path.position, multiply(path.direction, positive_width))
    right = subtract(path.position, multiply(path.direction, negative_width))

    return left, right


def get_underlay_boundaries(path: Path, inset: float):
    """
    Calculates the left and right boundary of a path, reduced by the size of 'inset'. Can be used for underlays.

    Args:
        path:  The path for which the underlay boundaries are calculated
        inset: The amount by which the underlay boundaries are smaller then the regular path boundaries

    Returns:
        left and right underlay boundary of a path
    """
    positive_width = multiply(path.width, path.stroke_alignment)
    negative_width = multiply(path.width, multiply(constant(-1), subtract(constant(1), path.stroke_alignment)))

    middle = multiply(constant(0.5), add(positive_width, negative_width))
    positive_width = maximum(subtract(positive_width, constant(inset)), middle)
    negative_width = minimum(add(negative_width, constant(inset)), middle)

    left = add(path.position, multiply(path.direction, positive_width))
    right = add(path.position, multiply(path.direction, negative_width))

    cut = inset / path.length

    left = repeat(1 - 2 * cut, shift(cut, left))
    right = repeat(1 - 2 * cut, shift(cut, right))

    return left, right
