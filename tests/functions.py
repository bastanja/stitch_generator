from stitch_generator.collection.functions.functions_1d import linear_0_1, linear_1_0, positive_sine, positive_cosine, \
    half_positive_sine, half_positive_cosine, half_circle, cubic_arc, three_stairs, half_peak
from stitch_generator.functions.function_sequence import function_sequence
from stitch_generator.functions.functions_1d import linear_interpolation, constant, square, arc, smoothstep, \
    smootherstep, circular_arc, sinus, cosinus, pchip_interpolation
from stitch_generator.functions.functions_2d import function_2d
from stitch_generator.functions.noise import noise
from stitch_generator.shapes.bezier import bezier_shape
from stitch_generator.shapes.circle import circle_shape
from stitch_generator.shapes.line import line_shape
from stitch_generator.shapes.spiral import spiral_shape

functions_1d_positive = {
    'linear_0_1': linear_0_1,
    'linear_1_0': linear_1_0,
    'positive_sine': positive_sine,
    'positive_cosine': positive_cosine,
    'half_positive_sine': half_positive_sine,
    'half_positive_cosine': half_positive_cosine,
    'half_peak': half_peak,
    'half_circle': half_circle,
    'cubic_arc': cubic_arc,
    'three_stairs': three_stairs,
    'const0': constant(0),
    'const0.5': constant(0.5),
    'const1': constant(1),
    'pchip': pchip_interpolation(((0, 1), (0.5, 0.2), (1, 1))),
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
    'circle': circle_shape(),
    'line': line_shape((0, 0), (10, 0)),
    'spiral': spiral_shape(10, 20, 2),
    'bezier': bezier_shape(((0, 0), (10, -10), (20, 0))),
    '2dconst': function_2d(constant(1), constant(0)),
    'bezier_seq': function_sequence(
        (bezier_shape(((0, 0), (10, -10), (20, 0))), bezier_shape(((20, 0), (30, 10), (40, 0)))),
        (1, 1))
}

all_functions = {**functions_1d, **functions_2d}
