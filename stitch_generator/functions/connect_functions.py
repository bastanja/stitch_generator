from functools import partial

import numpy as np

from stitch_generator.functions import sampling
from stitch_generator.functions.functions_2d import line
from stitch_generator.functions.sampling import regular_sampling
from stitch_generator.functions.types import ConnectFunction


def line_with_sampling_function(sampling_function):  # -> ConnectFunction
    return partial(_line_with_sampling_function, sampling_function=sampling_function)


def _line_with_sampling_function(p1, p2, sampling_function):
    p1, p2 = np.asarray(p1), np.asarray(p2)
    length = np.linalg.norm(p2 - p1)
    t = sampling_function(total_length=length)
    return line(p1, p2)(t)


def combine_start_end(connect_function: ConnectFunction) -> ConnectFunction:
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


def running_stitch_line(stitch_length: float, include_endpoint: bool):  # -> ConnectFunction
    return line_with_sampling_function(regular_sampling(stitch_length=stitch_length, include_endpoint=include_endpoint))


def presets(include_endpoint: bool, alignment: float):
    for s in iter(sampling.presets(include_endpoint, alignment)):
        yield line_with_sampling_function(s)
