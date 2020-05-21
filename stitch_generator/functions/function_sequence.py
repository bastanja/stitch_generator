import numpy as np

from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import combine
from stitch_generator.functions.functions_1d import linear_interpolation


def function_sequence(functions, lengths=None):
    lengths = _get_lengths(functions, lengths)
    mapped_functions = _get_mapped_functions(functions, lengths)
    dimension = _get_dimension(functions[0])
    if dimension > 1:
        return _get_sequence(mapped_functions, lengths, dimension)
    else:
        return _get_sequence_1d(mapped_functions, lengths)


def _get_mapped_functions(functions, lengths):
    low = 0
    mapped_functions = []
    for idx, f in enumerate(functions):
        high = lengths[idx]
        mapped_functions.append(combine(linear_interpolation(0, 1, low, high), f))
        low = high
    return mapped_functions


def _get_sequence(mapped_functions, lengths, dimension):
    def sequence(v):
        function_indices, v = _get_function_indices(v, lengths)
        result = np.zeros((len(v), dimension))
        _evaluate_functions(mapped_functions, function_indices, result, v)
        return result

    return sequence


def _get_sequence_1d(mapped_functions, lengths):
    def sequence(v):
        function_indices, v = _get_function_indices(v, lengths)
        result = np.zeros_like(v)
        _evaluate_functions(mapped_functions, function_indices, result, v)
        return result.T[0]

    return sequence


def _evaluate_functions(mapped_functions, function_indices, result, v):
    for j in range(len(mapped_functions)):
        result[function_indices == j] = mapped_functions[j](v[function_indices == j])


def _get_function_indices(v, lengths):
    v = np.asarray(v, dtype=float).reshape(-1, 1)
    function_indices = np.argmax(lengths[None, :] >= v, axis=1)
    return function_indices, v


def _get_dimension(function):
    dimension = len(function(0).reshape(-1, 1))
    return dimension


def _get_lengths(functions, lengths):
    if not lengths:
        try:
            lengths = [estimate_length(f) for f in functions]
        except np.AxisError:
            lengths = [1] * len(functions)

    lengths = np.cumsum(lengths).astype(float)
    lengths /= lengths[-1]
    return lengths


if __name__ == "__main__":
    from stitch_generator.functions.functions_2d import line
    from stitch_generator.functions.linspace import samples
    from stitch_generator.functions.functions_1d import constant

    seq = function_sequence((line(0, 10), line(10, 10, 0, 10), line(20, 10, 10, 10)))

    p = samples(30, True)
    print("--- 2D ---")
    print(seq(0.0))
    print(seq(p))

    print("--- 1D ---")
    seq2 = function_sequence((constant(0), linear_interpolation(0, 1), constant(1)), (1, 1, 1))
    print(seq2(0.0))
    print(seq2(p))
