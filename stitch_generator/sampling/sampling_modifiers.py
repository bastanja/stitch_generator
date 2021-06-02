import itertools

import numpy as np

from stitch_generator.functions.ensure_shape import ensure_1d_shape
from stitch_generator.functions.functions_1d import linear_interpolation
from stitch_generator.utilities.types import SamplingFunction


def free_start_end(start_length: float, end_length: float, sampling_function: SamplingFunction):
    """
    Returns samples where the start and end part are free of samples. Fills the inner part with samples from the
    sampling function
    """

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
    """
    Returns the samples from the sampling_function in alternating direction by reversing it on every second call
    """
    forward = itertools.cycle((True, False))

    def f(total_length: float):
        s = sampling_function(total_length)

        if not next(forward):
            s = np.flip(1 - s, axis=0)

        return s if include_endpoint else s[0:-1]

    return f


def ensure_start_end(samples, include_startpoint, include_endpoint):
    """
    Adds or removes the first and last sample to ensure that start and end sample are set as desired
    """
    # remove start point if not desired
    if np.isclose(samples[0], 0.0) and not include_startpoint:
        samples = samples[1:]
    # add start point if desired and missing
    if samples[0] > 0:
        samples = np.concatenate((ensure_1d_shape(0), samples))
    # remove end point if not desired
    if np.isclose(samples[-1], 1.0) and not include_endpoint:
        samples = samples[:-1]
    # add end point if desired and missing
    if samples[-1] < 1 and include_endpoint:
        samples = np.concatenate((samples, ensure_1d_shape(1)))

    return samples


def add_start_end(samples, include_startpoint, include_endpoint):
    """
    Ensures that the first sample is 0 if include_startpoint and that the last sample is 1 if include_endpoint
    Returns: the samples including 0 (if include_startpoint) and 1 (if include_endpoint)
    """
    # add start point if desired and missing
    if (len(samples) == 0 or samples[0] > 0) and include_startpoint:
        samples = np.concatenate((ensure_1d_shape(0), samples))
    # add end point if desired and missing
    if (len(samples) == 0 or samples[-1] < 1) and include_endpoint:
        samples = np.concatenate((samples, ensure_1d_shape(1)))

    return samples


def ensure_sample_at(sampling_function: SamplingFunction, sample_position: float):
    def f(total_length: float):
        s = sampling_function(total_length)

        delta = np.abs(s - sample_position)
        nearest_index = np.argmin(delta)
        s[nearest_index] = sample_position

        return s

    return f
