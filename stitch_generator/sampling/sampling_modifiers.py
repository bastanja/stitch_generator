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


def alternate_direction(sampling_function: SamplingFunction):
    """
    Returns the samples from the sampling_function in alternating direction by reversing it on every second call
    """
    forward = itertools.cycle((True, False))

    def modify(samples):
        if not next(forward) and len(samples) > 0:
            samples = np.flip(1 - samples, axis=0)

        return samples

    return modify_sampling(sampling_function, modify)


def modify_sampling(sampling_function, modify_samples):
    """
    Args:
        sampling_function: The sampling function to modify
        modify_samples: The modification that shall be applied to the samplesof the sampling function

    Returns:
        A new sampling function which returns the modified samples
    """

    def f(total_length: float):
        return modify_samples(sampling_function(total_length))

    return f


def ensure_sample_at(sampling_function: SamplingFunction, sample_position: float):
    """ Moves the sample which is nearest to sample_position exactly to sample_position """

    def modify(samples):
        if len(samples) == 0:
            return ensure_1d_shape(sample_position)
        delta = np.abs(samples - sample_position)
        nearest_index = np.argmin(delta)
        samples[nearest_index] = sample_position
        return samples

    return modify_sampling(sampling_function, modify)


def add_start(sampling_function: SamplingFunction) -> SamplingFunction:
    """ Adds a sample at the start if it is missing """

    def modify(samples):
        if len(samples) > 0:
            if not np.isclose(samples[0], 0):
                return np.concatenate((ensure_1d_shape(0), samples))
            else:
                return samples
        return ensure_1d_shape(0)

    return modify_sampling(sampling_function, modify)


def add_end(sampling_function: SamplingFunction) -> SamplingFunction:
    """ Adds a sample at the end if it is missing """

    def modify(samples):
        if len(samples) > 0:
            if not np.isclose(samples[-1], 1):
                return np.concatenate((samples, ensure_1d_shape(1)))
            else:
                return samples
        return ensure_1d_shape(1)

    return modify_sampling(sampling_function, modify)


def remove_start(sampling_function: SamplingFunction) -> SamplingFunction:
    """ Removes the first sample from the sampling function if it is close to the start """

    def modify(samples):
        if len(samples) > 0 and np.isclose(samples[0], 0):
            return samples[1:]
        return samples

    return modify_sampling(sampling_function, modify)


def remove_end(sampling_function: SamplingFunction) -> SamplingFunction:
    """ Removes the last sample from the sampling function if it is close to the end """

    def modify(samples):
        if len(samples) > 0 and np.isclose(samples[-1], 1):
            return samples[:-1]
        return samples

    return modify_sampling(sampling_function, modify)
