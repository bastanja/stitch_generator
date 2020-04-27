import numpy as np
from pytest import approx
from itertools import permutations

from lib.function_modifiers import repeat, reflect, wrap, nearest, combine, inverse, mix
from tests.functions import functions_1d, functions_2d, functions_1d_positive

offsets = [t / 10 for t in range(10)]
functions = functions_1d + functions_2d


def test_repeat():
    times = 2

    modes = ['reflect', 'wrap', 'nearest']

    for f in functions:
        for m in modes:
            r = repeat(times, f, mode=m)
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


def test_combine():
    pairs = permutations(functions_1d_positive, 2)
    v = np.linspace(0, 1, 10)
    for f1, f2 in pairs:
        f_combined = combine(f1, f2)

        v1 = f1(v)
        v2 = f2(v1)

        v_combined = f_combined(v)

        assert np.allclose(v2, v_combined)


def test_inverse():
    v = np.linspace(0, 1, 10)
    inv_v = 1 - v

    for f in functions_1d:
        inv_f = inverse(f)

        assert np.allclose(inv_f(v), f(inv_v))


def test_mix():
    combinations = permutations(functions_1d_positive, 3)
    v = np.linspace(0, 1, 10)
    for f1, f2, factor in combinations:
        factors = factor(v)
        v1 = f1(v)
        v2 = f2(v)

        mixed = mix(f1, f2, factor)

        v_mixed = v1 * (1 - factors) + v2 * factors

        assert np.allclose(v_mixed, mixed(v))
