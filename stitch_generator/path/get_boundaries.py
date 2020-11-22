from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import multiply, subtract, add, maximum, minimum, repeat, shift
from stitch_generator.functions.functions_1d import constant
from stitch_generator.path.path import Path


def get_boundaries(path: Path):
    positive_width = multiply(path.width, path.stroke_alignment)
    negative_width = multiply(path.width, subtract(constant(1), path.stroke_alignment))

    left = add(path.position, multiply(path.direction, positive_width))
    right = subtract(path.position, multiply(path.direction, negative_width))

    return left, right


def get_underlay_boundaries(path: Path, inset: float):
    positive_width = multiply(path.width, path.stroke_alignment)
    negative_width = multiply(path.width, multiply(constant(-1), subtract(constant(1), path.stroke_alignment)))

    middle = multiply(constant(0.5), add(positive_width, negative_width))
    positive_width = maximum(subtract(positive_width, constant(inset)), middle)
    negative_width = minimum(add(negative_width, constant(inset)), middle)

    left = add(path.position, multiply(path.direction, positive_width))
    right = add(path.position, multiply(path.direction, negative_width))

    cut = inset / estimate_length(path.position)

    left = repeat(1 - 2 * cut, shift(cut, left))
    right = repeat(1 - 2 * cut, shift(cut, right))

    return left, right
