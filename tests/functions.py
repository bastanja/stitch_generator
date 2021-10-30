import numpy as np

from stitch_generator.functions.function_1d_stairs import stairs
from stitch_generator.functions.function_sequence import function_sequence
from stitch_generator.functions.functions_1d import linear_interpolation, constant, square, arc, smoothstep, \
    smootherstep, circular_arc, sinus, cosinus, cubic_interpolation, pchip_interpolation
from stitch_generator.functions.functions_2d import function_2d
from stitch_generator.functions.noise import noise
from stitch_generator.shapes.bezier import bezier
from stitch_generator.shapes.circle import circle
from stitch_generator.shapes.line import line
from stitch_generator.shapes.spiral import spiral

functions_1d_positive = {
    'lin01': linear_interpolation(0, 1),
    'lin10': linear_interpolation(1, 0),
    'const0': constant(0),
    'const0.5': constant(0.5),
    'const1': constant(1),
    'cub': cubic_interpolation(((0, 0), (0.5, 1), (1, 0))),
    'pchip': pchip_interpolation(((0, 1), (0.5, 0.2), (1, 1))),
    'stair': stairs(np.linspace(0, 1, 6), 0.1),
    'square': square,
    'arc': arc,
    'smooth': smoothstep,
    'smoother': smootherstep,
    'circ': circular_arc,
    'seq': function_sequence((linear_interpolation(0, 1), constant(1)), (1, 1))
}

functions_1d_negative = {
    'sin': sinus,
    'cos': cosinus,
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
