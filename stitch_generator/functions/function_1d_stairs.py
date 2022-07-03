import itertools

from stitch_generator.functions.function_modifiers import chain
from stitch_generator.functions.function_sequence import function_sequence
from stitch_generator.functions.functions_1d import constant, linear_interpolation, smootherstep


def stairs(values, ascend_ratio):
    ascend_ratio = min(ascend_ratio, 0.5)
    straight_size = 1 - ascend_ratio * 2

    lengths = list(itertools.islice(itertools.cycle((straight_size, ascend_ratio * 2)), (len(values) * 2) - 1))
    lengths[0] += ascend_ratio
    lengths[-1] += ascend_ratio

    functions = [constant(values[0])]
    for previous, current in zip(values, values[1:]):
        step_function = chain(smootherstep, linear_interpolation(previous, current))
        functions.append(step_function)
        functions.append(constant(current))

    return function_sequence(functions, lengths)
