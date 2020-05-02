import numpy as np
from lib.functions_1d import cosinus, sinus, constant, linear_interpolation
from lib.function_modifiers import scale, add, repeat, multiply
from lib.bezier import de_casteljau
from stitch_effects.rotate import rotate_deg


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


def line(x, y, x0=0, y0=0):
    return function_2d(linear_interpolation(x0, x), linear_interpolation(y0, y))


def spiral(inner_radius, outer_radius, turns, center=(0, 0)):
    spiral = repeat(turns, circle(inner_radius, center))
    direction = repeat(turns, circle())
    increase = linear_interpolation(0, outer_radius - inner_radius)
    direction = multiply(direction, increase)
    spiral = add(spiral, direction)
    return spiral


def bezier(control_points):
    control_points = np.asarray(control_points, dtype=float)

    def f(v):
        points, tangents = de_casteljau(control_points, np.array(v, ndmin=1))
        return points

    return f


def bezier_normals(control_points):
    control_points = np.asarray(control_points, dtype=float)

    def f(v):
        points, tangents = de_casteljau(control_points, np.array(v, ndmin=1, dtype=float))
        return rotate_deg(tangents, -90)

    return f


def bezier_with_tangents(control_points):
    control_points = np.asarray(control_points, dtype=float)

    def f(v):
        points, tangents = de_casteljau(control_points, np.array(v, ndmin=1))
        return points, tangents

    return f
