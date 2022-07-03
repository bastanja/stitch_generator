import numpy as np

from stitch_generator.functions.ensure_shape import ensure_1d_shape
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import chain
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
        mapped_functions.append(chain(linear_interpolation(0, 1, low, high), f))
        low = high
    return mapped_functions


def _get_sequence(mapped_functions, lengths, dimension):
    def sequence(v):
        v_1d = ensure_1d_shape(np.asarray(v))
        function_indices = _get_function_indices(v_1d, ensure_1d_shape(lengths))
        result = np.zeros((len(v_1d), dimension))
        _evaluate_functions(mapped_functions, function_indices, result, v_1d)
        return result

    return sequence


def _get_sequence_1d(mapped_functions, lengths):
    def sequence(v):
        v = np.asarray(v)
        v_1d = ensure_1d_shape(v)
        function_indices = _get_function_indices(v_1d, ensure_1d_shape(lengths))
        result = np.zeros_like(v_1d)
        _evaluate_functions(mapped_functions, function_indices, result, v_1d)
        return result.reshape(v.shape)

    return sequence


def _evaluate_functions(mapped_functions, function_indices, result, v):
    for j in range(len(mapped_functions)):
        destination = result[function_indices == j]
        if len(destination) > 0:
            function_to_call = mapped_functions[j]
            parameter_to_use = v[function_indices == j]
            value = function_to_call(parameter_to_use)
            result[function_indices == j] = value


def _get_function_indices(v, lengths):
    return np.argmax(np.atleast_2d(lengths) >= np.atleast_2d(v).T, axis=1)


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
