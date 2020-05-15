from itertools import permutations

import numpy as np
from pytest import approx

from stitch_generator.functions.function_modifiers import repeat, reflect, wrap, nearest, combine, inverse, mix, add, \
    multiply
from tests.functions import all_functions, functions_1d, functions_1d_positive

offsets = [t / 10 for t in range(10)]
functions = all_functions


def test_repeat():
    times = 2

    modes = ['reflect', 'wrap', 'nearest']

    for name, f in functions.items():
        for m in modes:
            r = repeat(times, f, mode=m)
            for t in offsets:
                assert f(t) == approx(r(t / times))


def test_wrap():
    for name, f in functions.items():
        z = wrap(f)
        for t in offsets:
            assert f(t) == approx(z(t))
            assert f(t) == approx(z(t + 1))
            assert f(t) == approx(z(t + 2))
            assert f(t) == approx(z(t - 1))


def test_reflect():
    for name, f in functions.items():
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
    for name, f in functions.items():
        z = nearest(f)
        for t in offsets:
            assert f(t) == approx(z(t))
            assert f(0) == approx(z(t - 1))
            assert f(0) == approx(z(t - 2))
            assert f(1) == approx(z(t + 1))
            assert f(1) == approx(z(t + 2))


def test_combine():
    pairs = permutations(functions_1d_positive.values(), 2)
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

    for name, f in functions_1d.items():
        inv_f = inverse(f)

        assert np.allclose(inv_f(v), f(inv_v))


def test_mix():
    combinations = permutations(functions_1d_positive.values(), 3)
    v = np.linspace(0, 1, 10)
    for f1, f2, factor in combinations:
        factors = factor(v)
        v1 = f1(v)
        v2 = f2(v)

        mixed = mix(f1, f2, factor)

        v_mixed = v1 * (1 - factors) + v2 * factors

        assert np.allclose(v_mixed, mixed(v))


def test_add():
    pairs = permutations(all_functions.values(), 2)
    float_values = (0.0, 0.3, 0.5, 1.0)
    for f1, f2 in pairs:
        added = add(f1, f2)
        for v in float_values:
            assert np.allclose(added(v), f1(v) + f2(v))
        values = np.linspace(0, 1, 11)
        assert np.allclose(added(values), (f1(values).T + f2(values).T).T)


def test_multiply():
    pairs = permutations(all_functions.values(), 2)
    float_values = (0.0, 0.3, 0.5, 1.0)
    for f1, f2 in pairs:
        multiplied = multiply(f1, f2)
        for v in float_values:
            assert np.allclose(multiplied(v), f1(v) * f2(v))
        values = np.linspace(0, 1, 11)
        assert np.allclose(multiplied(values), (f1(values).T * f2(values).T).T)
