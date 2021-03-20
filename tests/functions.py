import numpy as np

from stitch_generator.functions.noise import noise
from stitch_generator.functions.function_1d_stairs import stairs
from stitch_generator.functions.function_sequence import function_sequence
from stitch_generator.functions.functions_1d import linear_interpolation, constant, cubic_interpolation_evenly_spaced, \
    square, arc, smoothstep, smootherstep, circular_arc, sinus, cosinus
from stitch_generator.functions.functions_2d import circle, line, spiral, bezier, function_2d

functions_1d_positive = {
    'lin01': linear_interpolation(0, 1),
    'lin10': linear_interpolation(1, 0),
    'const0': constant(0),
    'const0.5': constant(0.5),
    'const1': constant(1),
    'cub': cubic_interpolation_evenly_spaced([0, 1, 0]),
    'stair': stairs(np.linspace(0, 1, 6), 0.1),
    'square': square(),
    'arc': arc(),
    'smooth': smoothstep(),
    'smoother': smootherstep(),
    'circ': circular_arc(),
    'seq': function_sequence((linear_interpolation(0, 1), constant(1)), (1, 1))
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
    '2dconst': function_2d(constant(1), constant(0)),
    'bezier_seq': function_sequence((bezier(((0, 0), (10, -10), (20, 0))), bezier(((20, 0), (30, 10), (40, 0)))),
                                    (1, 1))
}

all_functions = {**functions_1d, **functions_2d}
