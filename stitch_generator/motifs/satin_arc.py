import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.functions.connect_functions import simple_connect
from stitch_generator.functions.function_modifiers import scale, combine
from stitch_generator.functions.functions_1d import arc, linear_interpolation, constant
from stitch_generator.functions.functions_2d import function_2d, constant_direction
from stitch_generator.sampling.sample_by_number import sampling_by_number
from stitch_generator.stitch_effects.utilities.satin import satin_along


def satin_arc(length: float, height: float, start_thickness: float, middle_thickness: float, spacing=0.5):
    path = Path(shape=function_2d(linear_interpolation(0, length), scale(-height, arc)),
                direction=constant_direction(0, 1),
                width=combine(arc, linear_interpolation(start_thickness, middle_thickness)),
                stroke_alignment=constant(0))
    samples = length / spacing
    samples = int(samples / 2) * 2
    sampling = sampling_by_number(samples, include_endpoint=True)

    stitches = np.concatenate(
        (path.shape(0), satin_along(path, sampling_function=sampling, connect_function=simple_connect)))
    return stitches
