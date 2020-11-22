import itertools

import numpy as np

from stitch_generator.functions.functions_1d import linear_interpolation
from stitch_generator.functions.types import SamplingFunction


def free_start_end(start_length: float, end_length: float, sampling_function: SamplingFunction):
    def f(total_length: float):
        cut_length = start_length + end_length
        if total_length > cut_length:
            start_offset = linear_interpolation(0, 1, 0, total_length)(start_length)
            sampled_part = total_length - cut_length
            scale = sampled_part / total_length
            samples = sampling_function(total_length - cut_length) * scale
            return samples + start_offset
        else:
            return np.array((), ndmin=2)

    return f


def alternate_direction(sampling_function: SamplingFunction, include_endpoint: bool):
    forward = itertools.cycle((True, False))

    def f(total_length: float):
        s = sampling_function(total_length)

        if not next(forward):
            s = np.flip(1 - s, axis=0)

        return s if include_endpoint else s[0:-1]

    return f
