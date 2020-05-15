from stitch_generator.functions.function_modifiers import repeat, multiply, add
from stitch_generator.functions.functions_1d import constant, linear_interpolation, stairs


def repeat_with_offset(position, direction, width, repetitions, stair_ratio, circular=False):
    if circular:
        mode = 'wrap'
        offset = linear_interpolation(-0.5, 0.5)
    else:
        mode = 'reflect'
        offset = add(stairs(repetitions, stair_ratio), constant(-0.5))

    f = repeat(repetitions, position, mode)
    direction = repeat(repetitions, direction, mode)
    width = repeat(repetitions, width, mode)

    offset = multiply(offset, width)
    direction = multiply(direction, offset)

    f = add(f, direction)
    return f, direction, width
