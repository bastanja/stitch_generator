import numpy as np
import pytest

from lib.functions_1d import linear_interpolation, constant, sinus, cosinus, cubic_interpolation_evenly_spaced, \
    stairs, square, arc, smoothstep, smootherstep
from pytest import approx
from tests.functions import functions_1d

def test_constant():
    c = 0.123
    f = constant(c)
    for i in range(10):
        assert f(i / 10) == c


def test_linear_interpolation():
    # interpolation range [0;1] (source range not set)
    f = linear_interpolation(0, 10)

    # test values in interpolation range [0;1]
    assert f(0) == approx(0)
    assert f(0.5) == approx(5)
    assert f(1) == approx(10)

    # test values outside interpolation range
    assert f(-1) == approx(-10)
    assert f(2) == approx(20)

    # test input range [0;5]
    f = linear_interpolation(0, 10, 0, 5)
    assert f(0) == approx(0)
    assert f(0.5) == approx(1)
    assert f(2.5) == approx(5)
    assert f(10) == approx(20)

    # test inverting of values
    f = linear_interpolation(1, 0, 0, 1)
    assert f(0) == approx(1)
    assert f(0.25) == approx(0.75)
    assert f(1) == approx(0)

    # test with negative values
    f = linear_interpolation(-1, 1)
    assert f(0) == approx(-1)
    assert f(0.5) == approx(0)
    assert f(1) == approx(1)

    # test with invalid target range
    f = linear_interpolation(1, 1)
    assert f(0) == approx(1)
    assert f(0.5) == approx(1)
    assert f(1) == approx(1)

    # test with invalid source range
    f = linear_interpolation(0, 2, 1, 1)
    assert f(0) == approx(0)
    assert f(0.5) == approx(0)
    assert f(1) == approx(0)


def test_sinus():
    f = sinus()
    # check that full sinus curve is mapped to range [0;1]
    assert f(0) == approx(0)
    assert f(0.25) == approx(1)
    assert f(0.5) == approx(0)
    assert f(0.75) == approx(-1)
    assert f(1) == approx(0)

    # test outside the range [0;1]
    assert f(2) == approx(f(1))
    assert f(-1) == approx(f(1))


def test_cosinus():
    f = cosinus()
    # check that full cosinus curve is mapped to range [0;1]
    assert f(0) == approx(1)
    assert f(0.25) == approx(0)
    assert f(0.5) == approx(-1)
    assert f(0.75) == approx(0)
    assert f(1) == approx(1)

    # test outside the range [0;1]
    assert f(2) == approx(f(1))
    assert f(-1) == approx(f(1))


def test_cubic_interpolation_evenly_spaced():
    f = cubic_interpolation_evenly_spaced([1, 2, 0, 3, 5])
    assert f(0) == approx(1)
    assert f(0.25) == approx(2)
    assert f(0.5) == approx(0)
    assert f(0.75) == approx(3)
    assert f(1) == approx(5)

    f = cubic_interpolation_evenly_spaced([1, 2])
    assert f(0) == approx(1)
    assert f(0.5) == approx(1.5)
    assert f(1) == approx(2)

    # expect that the interpolation is not defined outside the range [0;1]
    with pytest.raises(Exception):
        f(2)

    # expect that interpolation is not possible with only one value
    with pytest.raises(Exception):
        f = cubic_interpolation_evenly_spaced([2])


def test_stairs():
    steps = 2
    ratio = 0.1
    f = stairs(steps, ratio)
    assert f(0) == approx(0)
    assert f(0.5) == approx(0.5)
    assert f(1) == approx(1)

    step_increase_size = ratio / steps
    assert f(0.5 - step_increase_size) == approx(0)
    assert f(0.5 + step_increase_size) == approx(1)

    steps = 2
    ratio = 0.1
    f = stairs(steps, ratio)
    assert f(0) == approx(0)
    assert f(0.5) == approx(0.5)
    assert f(1) == approx(1)

    step_increase_size = ratio / steps
    assert f(0.5 - step_increase_size) == approx(0)
    assert f(0.5 + step_increase_size) == approx(1)

    steps = 3
    ratio = 0.1
    f = stairs(steps, ratio)
    assert f(0) == approx(0)
    assert f(1 / 3) == approx(0.25)
    assert f(0.5) == approx(0.5)
    assert f(2 / 3) == approx(0.75)
    assert f(1) == approx(1)

    step_increase_size = ratio / steps
    assert f((1 / 3) - step_increase_size) == approx(0)
    assert f((1 / 3) + step_increase_size) == approx(0.5)


def test_square():
    f = square()
    assert f(0) == approx(0)
    assert f(0.5) == approx(0.25)
    assert f(1) == approx(1)


def test_arc():
    f = arc()
    assert f(0) == approx(0)
    assert f(0.5) == approx(1)
    assert f(1) == approx(0)


def test_smoothstep():
    f = smoothstep()
    assert (f(0) == approx(0))
    assert (f(0.5) == approx(0.5))
    assert (f(1) == approx(1))


def test_smootherstep():
    f = smootherstep()
    assert (f(0) == approx(0))
    assert (f(0.5) == approx(0.5))
    assert (f(1) == approx(1))


def test_with_float_value():
    for f in functions_1d:
        result = f(0.5)
        assert -1 <= result <= 1


def test_with_np_aray():
    values = np.array([0, 0.5, 1])
    for f in functions_1d:
        result = f(values)
        assert len(result) == len(values)

        plain_result = [f(v) for v in [0, 0.5, 1]]
        assert np.allclose(result, plain_result)
