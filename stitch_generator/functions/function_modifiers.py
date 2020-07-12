import numpy as np

from stitch_generator.functions.ensure_shape import ensure_1d_shape


def reflect(function):
    def f(v):
        val = 1 - (np.absolute(1 - (v % 2)))
        return function(val)

    return f


def wrap(function):
    return lambda v: function(v % 1)


def nearest(function):
    def f(v):
        if v < 0: v = 0
        if v > 1: v = 1
        return function(v)

    return f


def repeat(r, function, mode=''):
    if mode == 'reflect':
        function = reflect(function)
    if mode == 'wrap':
        function = wrap(function)
    if mode == 'nearest':
        function = nearest(function)
    return lambda v: function(np.asarray(v) * r)


def scale(s, function):
    return lambda v: function(v) * s


def shift(amount, function):
    return lambda v: function(v + amount)


def combine(f1, f2):
    return lambda v: f2(f1(v))


def add(f1, f2):
    return _binary_operation(lambda a, b: a + b, f1, f2)


def subtract(f1, f2):
    return _binary_operation(lambda a, b: a - b, f1, f2)


def multiply(f1, f2):
    return _binary_operation(lambda a, b: a * b, f1, f2)


def inverse(f):
    return lambda v: f(1 - v)


def mix(f1, f2, factor):
    def f(v):
        fv = factor(v)
        return f1(v) * (1 - fv) + f2(v) * fv

    return f


def _binary_operation(operation, f1, f2):
    def f(v):
        v = ensure_1d_shape(v)
        v1 = f1(v)
        v2 = f2(v)
        try:
            result = operation(v1, v2)
        except ValueError:
            # Transpose operands, apply operation and transpose result back
            result = operation(v1.T, v2.T).T
        return result

    return f


def maximum(f1, f2):
    return lambda v: np.maximum(f1(v), f2(v))


def minimum(f1, f2):
    return lambda v: np.minimum(f1(v), f2(v))
