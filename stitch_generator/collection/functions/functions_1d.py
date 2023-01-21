from stitch_generator.functions.function_1d_stairs import stairs
from stitch_generator.functions.function_modifiers import subtract, repeat, chain
from stitch_generator.functions.functions_1d import constant, linear_interpolation, arc, circular_arc, sinus, \
    cubic_interpolation, smoothstep
from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number

linear_0_1 = linear_interpolation(0, 1)
linear_1_0 = linear_interpolation(1, 0)

positive_sine = chain(sinus, linear_interpolation(0, 1, source_low=-1, source_high=1))
positive_cosine = chain(sinus, linear_interpolation(0, 1, source_low=-1, source_high=1))
half_positive_sine = repeat(0.5, positive_sine)
half_positive_cosine = repeat(0.5, positive_cosine)

half_peak = subtract(constant(1.0), repeat(0.5, arc, mode='reflect'))
half_smoothstep = chain(repeat(0.5, smoothstep), linear_interpolation(0, 1, source_low=0, source_high=0.5))

half_circle = repeat(2, circular_arc, mode='reflect')

cubic_arc = cubic_interpolation(((0, 0), (0.5, 1), (1, 0)))
three_stairs = stairs(values=subdivide_by_number(3), ascend_ratio=0.1)
