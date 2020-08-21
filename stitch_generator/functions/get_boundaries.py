from stitch_generator.functions.function_modifiers import multiply, subtract, add
from stitch_generator.functions.functions_1d import constant
from stitch_generator.functions.path import Path


def get_boundaries(path: Path):
    pos_width = multiply(path.width, path.stroke_alignment)
    neg_width = multiply(path.width, subtract(constant(1), path.stroke_alignment))

    left = add(path.position, multiply(path.direction, pos_width))
    right = subtract(path.position, multiply(path.direction, neg_width))

    return left, right
