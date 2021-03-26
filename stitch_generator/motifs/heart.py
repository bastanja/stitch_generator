import numpy as np

from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import scale
from stitch_generator.functions.function_sequence import function_sequence
from stitch_generator.sampling.sample_by_length import sample_by_length
from stitch_generator.shapes.bezier import bezier


def heart(size: float = 8, stitch_length: float = 2):
    curve = function_sequence((bezier(((-4, 0), (0, -1), (2.92, -4.51), (3.94, -6.72))),
                               bezier(((3.94, -6.72), (5.27, -9.61), (1.16, -11.53), (0.01, -8.39)))))
    curve = scale(size / 8, curve)
    half_heart = curve(sample_by_length(estimate_length(curve), stitch_length, include_endpoint=True))
    full_heart = np.concatenate((half_heart[:-1], half_heart[::-1] * (-1, 1)))
    return full_heart
