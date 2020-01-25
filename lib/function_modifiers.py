import math


def zigzag(function):
    def f(v):
        val = 1 - (math.fabs(1 - (v % 2)))
        return function(val)

    return f


def mod1(function):
    return lambda v: function(v % 1)


def clamp1(function):
    def f(v):
        if v < 0: v = 0
        if v > 1: v = 1
        return function(v)

    return f


def repeat(r, function, mode=''):
    if mode == 'zigzag':
        function = zigzag(function)
    if mode == 'mod1':
        function = mod1(function)
    if mode == 'clamp1':
        function = clamp1(function, 0, 1)
    return lambda v: function(v * r)


def scale(s, function):
    return lambda v: function(v) * s


def shift(amount, function):
    return lambda v: function(v + amount)


def combine(f1, f2):
    return lambda v: f1(f2(v))


def add(f1, f2):
    return lambda v: f1(v) + f2(v)


def multiply(f1, f2):
    return lambda v: f1(v) * f2(v)


def inverse(f):
    return lambda v: f(1 - v)
