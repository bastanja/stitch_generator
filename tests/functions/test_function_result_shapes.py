import numpy as np
import pytest

from stitch_generator.functions import (
    add_functions,
    constant,
    divide_functions,
    function_3d,
    function_sequence,
    linear_interpolation,
    mix,
    multiply_functions,
    sinus,
    subtract_functions,
)
from stitch_generator.shapes import bezier_shape, line_shape
from tests.functions.functions import functions_2d, functions_1d

single_value = 0.4
single_value_parameters = [
    single_value,
    np.array(single_value, ndmin=1),
    np.array(single_value, ndmin=2),
]

multiple_values = (0, 0.3, 0.7, 1)
length = len(multiple_values)
multiple_values_parameters = [
    multiple_values,
    np.array(multiple_values, ndmin=1),
    np.array(multiple_values, ndmin=2),
    np.array(multiple_values, ndmin=2).T,
]

empty_parameters = [(), np.array([])]


def combined_functions(f):
    return {
        "add": add_functions(f, f),
        "subtract": subtract_functions(f, f),
        "multiply": multiply_functions(f, constant(2)),
        "divide": divide_functions(f, constant(2)),
        "mix": mix(f, f, constant(0.5)),
    }


line_2d = line_shape((0, 0), (10, 0))
all_functions_2d = {**functions_2d, **combined_functions(line_2d)}

line_3d = line_shape((0, 0, 0), (10, 0, 5))
bezier_3d = bezier_shape(((0, 0, 0), (10, -10, 5), (20, 0, 10)))
all_functions_3d = {
    "line": line_3d,
    "bezier": bezier_3d,
    "3dconst": function_3d(constant(1), constant(0), constant(2)),
    "3dfunc": function_3d(linear_interpolation(0, 10), sinus, constant(1)),
    "bezier_seq": function_sequence(
        (bezier_3d, bezier_shape(((20, 0, 10), (30, 10, 5), (40, 0, 0)))), (1, 1)
    ),
    **combined_functions(line_3d),
}


@pytest.mark.parametrize("name, f", all_functions_2d.items())
def test_shapes_2d(name, f):
    _test_nd_single_parameter(f, dimension=2)
    _test_nd_multiple_parameters(f, dimension=2)
    _test_nd_empty_parameters(f, dimension=2)


@pytest.mark.parametrize("name, f", all_functions_3d.items())
def test_shapes_3d(name, f):
    _test_nd_single_parameter(f, dimension=3)
    _test_nd_multiple_parameters(f, dimension=3)
    _test_nd_empty_parameters(f, dimension=3)


@pytest.mark.parametrize("name, f", functions_1d.items())
def test_shapes_1d(name, f):
    _test_1d_single_parameter(f)
    _test_1d_multiple_parameters(f)
    _test_1d_empty_parameters(f)


def _test_nd_single_parameter(function, dimension):
    for p in single_value_parameters:
        result = function(p)
        assert result.shape == (1, dimension)


def _test_nd_multiple_parameters(function, dimension):
    for p in multiple_values_parameters:
        result = function(p)
        assert result.shape == (length, dimension)


def _test_nd_empty_parameters(function, dimension):
    for p in empty_parameters:
        result = function(p)
        assert result.shape == (0, dimension)


def _test_1d_single_parameter(function):
    for p in single_value_parameters:
        result = function(p)
        assert result.shape == np.asarray(p).shape


def _test_1d_multiple_parameters(function):
    for p in multiple_values_parameters:
        result = function(p)
        assert result.shape == np.asarray(p).shape


def _test_1d_empty_parameters(function):
    for p in empty_parameters:
        result = function(p)
        assert result.shape == (0,)
