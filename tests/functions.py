from stitch_generator.functions.functions_1d import linear_interpolation, constant, cubic_interpolation_evenly_spaced, \
    stairs, square, arc, smoothstep, smootherstep, circular_arc, sinus, cosinus, noise
from stitch_generator.functions.functions_2d import circle, line, spiral, bezier, function_2d

functions_1d_positive = {
    'lin01': linear_interpolation(0, 1),
    'lin10': linear_interpolation(1, 0),
    'const0': constant(0),
    'const0.5': constant(0.5),
    'const1': constant(1),
    'cub': cubic_interpolation_evenly_spaced([0, 1, 0]),
    'stair': stairs(5, 0.1),
    'square': square(),
    'arc': arc(),
    'smooth': smoothstep(),
    'smoother': smootherstep(),
    'circ': circular_arc()
}

functions_1d_negative = {
    'sin': sinus(),
    'cos': cosinus(),
    'noise': noise()
}

functions_1d = {**functions_1d_positive, **functions_1d_negative}

functions_2d = {
    'circle': circle(),
    'line': line((0, 0), (10, 0)),
    'spiral': spiral(10, 20, 2),
    'bezier': bezier(((0, 0), (10, -10), (20, 0))),
    '2dconst': function_2d(constant(1), constant(0))
}

all_functions = {**functions_1d, **functions_2d}
