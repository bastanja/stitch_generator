import numpy as np

from stitch_generator.functions.function_sequence import function_sequence
from stitch_generator.functions.functions_1d import constant, linear_interpolation
from stitch_generator.functions.functions_2d import line, bezier
from stitch_generator.sampling.sample_by_number import sample_by_number


def test_function_sequence_1d():
    t = sample_by_number(5, True)
    functions = (constant(0), linear_interpolation(0, 1), constant(1))
    lengths = (1, 1, 1)
    sequence = function_sequence(functions, lengths)
    single_value = sequence(0.0)
    array_values = sequence(t)

    # check that we get a 1d array when we call function_sequence with a single value
    assert type(single_value) == np.ndarray
    assert len(single_value.shape) == 0

    # check that we get a 1d array when we call function_sequence with an array of values
    assert type(array_values) == np.ndarray
    assert len(array_values.shape) == 1

    # check resulting values
    assert np.allclose(sequence(0), 0)
    assert np.allclose(sequence(1 / 3), 0)
    assert np.allclose(sequence(0.5), 0.5)
    assert np.allclose(sequence(2 / 3), 1)
    assert np.allclose(sequence(1), 1)


def test_function_sequence_2d():
    t = sample_by_number(5, True)
    functions = (line((0, 0), (0, 10)), line((0, 10), (10, 10)), line((10, 10), (20, 10)))
    sequence = function_sequence(functions)
    single_value = sequence(0.0)
    array_values = sequence(t)

    # check that we get a 2d array when we call function_sequence with a single value
    assert type(single_value) == np.ndarray
    assert len(single_value.shape) == 2

    # check that we get a 2d array when we call function_sequence with an array of values
    assert type(array_values) == np.ndarray
    assert len(array_values.shape) == 2

    assert single_value.shape[1] == array_values.shape[1]


def test_function_sequence_bezier():
    t = sample_by_number(5, True)
    points_1 = ((0, 0), (10, 10), (20, 10))
    points_2 = ((20, 10), (30, -10), (40, 0))
    functions = (bezier(points_1), bezier(points_2))
    sequence = function_sequence(functions)
    single_value = sequence(0.0)
    array_values = sequence(t)

    # check that we get a 2d array when we call function_sequence with a single value
    assert type(single_value) == np.ndarray
    assert len(single_value.shape) == 2

    # check that we get a 2d array when we call function_sequence with an array of values
    assert type(array_values) == np.ndarray
    assert len(array_values.shape) == 2

    assert single_value.shape[1] == array_values.shape[1]
