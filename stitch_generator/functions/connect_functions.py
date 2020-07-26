from functools import partial

import numpy as np

from stitch_generator.functions.functions_2d import line
from stitch_generator.functions.samples import samples_by_fixed_length_with_alignment, samples_by_length


def line_with_sampling_function(sampling_function):
    return partial(_line_with_sampling_function, sampling_function=sampling_function)


def line_constant_stitch_length(stitch_length, include_endpoint: bool):
    sampling_function = partial(samples_by_length, segment_length=stitch_length, include_endpoint=include_endpoint)
    return partial(_line_with_sampling_function, sampling_function=sampling_function)


def line_fixed_stitch_length(stitch_length, alignment, include_endpoint: bool):
    sampling_function = partial(samples_by_fixed_length_with_alignment, segment_length=stitch_length,
                                alignment=alignment, include_endpoint=include_endpoint)
    return partial(_line_with_sampling_function, sampling_function=sampling_function)


def combine_start_end(connect_function):
    last_point = None

    def f(p1, p2):
        points = connect_function(p1, p2)

        nonlocal last_point
        try:
            points[0] = (points[0] + last_point) / 2
        except TypeError:
            # if last_point was not set yet, ignore it
            pass

        last_point = points[-1]
        return points[0: -1]

    return f


def _line_with_sampling_function(p1, p2, sampling_function):
    length = np.linalg.norm(p2 - p1)
    t = sampling_function(total_length=length)
    return line(p1, p2)(t)
