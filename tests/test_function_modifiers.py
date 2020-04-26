from pytest import approx

from lib.function_modifiers import repeat, reflect, wrap, nearest
from lib.functions_1d import linear_interpolation, sinus, noise
from lib.functions_2d import circle, line

functions = [linear_interpolation(1, 2), sinus(), noise(), circle(), line(10, 20)]
offsets = [t / 10 for t in range(10)]


def test_repeat():
    times = 2
    for f in functions:
        r = repeat(times, f)
        for t in offsets:
            assert f(t) == approx(r(t / times))


def test_wrap():
    for f in functions:
        z = wrap(f)
        for t in offsets:
            assert f(t) == approx(z(t))
            assert f(t) == approx(z(t + 1))
            assert f(t) == approx(z(t + 2))
            assert f(t) == approx(z(t - 1))


def test_reflect():
    for f in functions:
        z = reflect(f)
        for t in offsets:
            assert f(t) == approx(z(t))
            assert f(t) == approx(z(2 - t))
            assert f(t) == approx(z(2 + t))
            assert f(t) == approx(z(4 - t))
            assert f(t) == approx(z(4 + t))
            assert f(t) == approx(z(-2 - t))
            assert f(t) == approx(z(-2 + t))


def test_nearest():
    for f in functions:
        z = nearest(f)
        for t in offsets:
            assert f(t) == approx(z(t))
            assert f(0) == approx(z(t - 1))
            assert f(0) == approx(z(t - 2))
            assert f(1) == approx(z(t + 1))
            assert f(1) == approx(z(t + 2))
