import numpy as np
from lib.functions_1d import cosinus, sinus, constant, linear_interpolation
from lib.function_modifiers import scale, add, repeat, multiply
from lib.bezier import de_casteljau


def function_2d(fx, fy):
    return lambda t: np.array([fx(t), fy(t)]).T


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


def spiral(inner_radius, outer_radius, turns, center=(0, 0)):
    spiral = repeat(turns, circle(inner_radius, center))
    direction = repeat(turns, circle())
    increase = linear_interpolation(0, outer_radius - inner_radius)
    direction = multiply(direction, increase)
    spiral = add(spiral, direction)
    return spiral


def bezier(control_points):
    def f(v):
        points, tangents = de_casteljau(control_points, np.array(v, ndmin=1))
        return points
    return f


def bezier_with_tangents(control_points):
    def f(v):
        points, tangents = de_casteljau(control_points, np.array(v, ndmin=1))
        return points, tangents
    return f
