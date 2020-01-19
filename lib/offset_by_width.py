from lib.function_modifiers import multiply, add
from lib.functions_1d import constant


def offset_by_width(position, direction, width, negative_direction: bool, factor: float):
    if negative_direction:
        factor = -factor

    if factor != 1:
        direction = multiply(direction, constant(factor))

    direction = multiply(direction, width)
    position = add(position, direction)

    return position


def offset_half_width(position, direction, width):
    return offset_by_width(position, direction, width, True, 0.5)
