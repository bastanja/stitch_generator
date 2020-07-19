from stitch_generator.functions.function_modifiers import multiply, subtract, add
from stitch_generator.functions.functions_1d import constant


def get_boundaries(f, direction, width, offset):
    pos_width = multiply(width, offset)
    neg_width = multiply(width, subtract(constant(1), offset))

    f1 = add(f, multiply(direction, pos_width))
    f2 = subtract(f, multiply(direction, neg_width))

    return f1, f2
