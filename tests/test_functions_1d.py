from lib.functions_1d import linear_interpolation, constant, sinus, cosinus, noise
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
    s = sinus()
    # check that full sinus curve is mapped to range [0;1]
    assert s(0) == approx(0)
    assert s(0.25) == approx(1)
    assert s(0.5) == approx(0)
    assert s(0.75) == approx(-1)
    assert s(1) == approx(0)


def test_cosinus():
    c = cosinus()
    # check that full cosinus curve is mapped to range [0;1]
    assert c(0) == approx(1)
    assert c(0.25) == approx(0)
    assert c(0.5) == approx(-1)
    assert c(0.75) == approx(0)
    assert c(1) == approx(1)


