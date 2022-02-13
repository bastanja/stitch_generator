from stitch_generator.functions.function_modifiers import subtract, add, scale, repeat
from stitch_generator.functions.functions_1d import constant, linear_interpolation, cosinus, arc, circular_arc

half_cosine_positive = add(constant(0.5), scale(0.5, repeat(0.5, cosinus)))
linear_0_1 = linear_interpolation(0, 1)
half_peak = subtract(constant(1), repeat(0.5, arc, mode='reflect'))
half_circle = repeat(2, circular_arc, mode='reflect')
