from functools import partial

import numpy as np

from stitch_generator.functions.ensure_shape import ensure_2d_shape
from stitch_generator.sampling.sample_by_length import sampling_by_length
from stitch_generator.sampling.sampling_modifiers import remove_end
from stitch_generator.shapes.line import line
from stitch_generator.framework.types import ConnectFunction


def simple_connect(p1, p2):
    return ensure_2d_shape(p2)


def line_with_sampling_function(sampling_function):  # -> ConnectFunction
    return partial(_line_with_sampling_function, sampling_function=sampling_function)


def running_stitch_line(stitch_length: float, include_endpoint: bool):  # -> ConnectFunction
    sampling_function = sampling_by_length(segment_length=stitch_length)
    if not include_endpoint:
        sampling_function = remove_end(sampling_function)
    return line_with_sampling_function(sampling_function)


def _line_with_sampling_function(p1, p2, sampling_function):
    p1, p2 = np.asarray(p1), np.asarray(p2)
    length = np.linalg.norm(p2 - p1)
    t = sampling_function(total_length=length)
    return line(p1, p2)(t)


def combine_start_end(connect_function: ConnectFunction) -> ConnectFunction:
    """
    Combines the end point of the previous call of the connect function with the start point of the current call.
    Averages their position and sets it as start point of the current connection.
    """
    last_point = None

    def f(p1, p2):
        points = connect_function(p1, p2)
        if len(points) == 0:
            return points

        nonlocal last_point
        try:
            points[0] = (points[0] + last_point) / 2
        except TypeError:
            # if last_point was not set yet, ignore it
            pass

        last_point = points[-1]
        return points[0: -1]

    return f
