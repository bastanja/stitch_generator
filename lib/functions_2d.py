from lib.functions_1d import cosinus, sinus, constant, linear_interpolation
from lib.function_modifiers import scale, add


def function_2d(fx, fy):
    return lambda t: (fx(t), fy(t))


def circle(radius=1, center=(0, 0)):
    fx = cosinus()
    fy = sinus()
    f = function_2d(fx, fy)
    if radius != 1:
        f = scale(radius, f)
    if center != (0, 0):
        c = function_2d(constant(center[0]), constant(center[1]))
        f = add(f, c)
    return f


def line(x, y):
    return function_2d(linear_interpolation(0, x), linear_interpolation(0, y))