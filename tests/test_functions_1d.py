import pytest

from lib.functions_1d import linear_interpolation, constant, sinus, cosinus, noise, cubic_interpolation_evenly_spaced
from pytest import approx


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
