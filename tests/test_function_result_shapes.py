import numpy as np

from tests.functions import functions_2d, functions_1d

single_value = 0.4
single_value_parameters = [
    single_value,
    np.array(single_value, ndmin=1),
    np.array(single_value, ndmin=2)
]

multiple_values = (0, 0.3, 0.7, 1)
length = len(multiple_values)
multiple_values_parameters = [
    multiple_values,
    np.array(multiple_values, ndmin=1),
    np.array(multiple_values, ndmin=2),
    np.array(multiple_values, ndmin=2).T
]


def test_shapes_2d():
    for name, f in functions_2d.items():
        _test_2d_single_parameter(f)
        _test_2d_multiple_parameters(f)


def test_shapes_1d():
    for name, f in functions_1d.items():
        _test_1d_single_parameter(f)
        _test_1d_multiple_parameters(f)


def _test_2d_single_parameter(function):
    for p in single_value_parameters:
        result = function(p)
        assert result.shape == (1, 2)


def _test_2d_multiple_parameters(function):
    for p in multiple_values_parameters:
        result = function(p)
        assert result.shape == (length, 2)


def _test_1d_single_parameter(function):
    for p in single_value_parameters:
        result = function(p)
        assert result.shape == np.asarray(p).shape


def _test_1d_multiple_parameters(function):
    for p in multiple_values_parameters:
        result = function(p)
        assert result.shape == np.asarray(p).shape
