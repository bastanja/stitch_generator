from lib.functions_1d import *
from lib.functions_2d import circle, line

functions_1d_positive = [
    linear_interpolation(0, 1),
    linear_interpolation(1, 0),
    constant(0),
    constant(0.5),
    constant(1),
    cubic_interpolation_evenly_spaced([0, 1, 0]),
    stairs(5, 0.1),
    square(),
    arc(),
    smoothstep(),
    smootherstep(),
    circular_arc()
]

functions_1d = functions_1d_positive + [
    sinus(),
    cosinus(),
    noise()
]

functions_2d = [
    circle(),
    line(10, 0)
]
