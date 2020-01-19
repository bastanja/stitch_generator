from lib.functions_1d import constant, linear_interpolation, stairs
from lib.function_modifiers import repeat, multiply, add


def repeat_with_offset(position, direction, width, repetitions, stair_ratio, circular=False):
    if circular:
        mode = 'mod1'
        offset = linear_interpolation(-0.5, 0.5)
    else:
        mode = 'zigzag'
        offset = add(stairs(repetitions, stair_ratio), constant(-0.5))

    f = repeat(repetitions, position, mode)
    direction = repeat(repetitions, direction, mode)
    width = repeat(repetitions, width, mode)

    offset = multiply(offset, width)
    direction = multiply(direction, offset)

    f = add(f, direction)
    return f, direction, width
