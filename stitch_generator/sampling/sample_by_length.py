import numpy as np

from stitch_generator.framework.types import SamplingFunction, Array1D
from stitch_generator.sampling.sample_by_number import sample_by_number


def sample_by_length(total_length: float, segment_length: float) -> Array1D:
    if np.isclose(total_length, 0) or (segment_length > total_length) or np.isclose(segment_length, 0):
        return sample_by_number(1)

    number_of_segments = int(round(total_length / segment_length))
    return sample_by_number(number_of_segments=number_of_segments)


def sampling_by_length(segment_length: float) -> SamplingFunction:
    def f(total_length: float):
        return sample_by_length(total_length=total_length, segment_length=segment_length)

    return f


def sample_by_length_with_offset(total_length: float, segment_length: float, offset: float) -> Array1D:
    segment_to_length = segment_length / total_length if total_length > 0 else 0
    offset = (offset % 1) * segment_to_length

    samples = sample_by_length(total_length=total_length, segment_length=segment_length)[:-1] + offset
    return samples


def sampling_by_length_with_offset(segment_length: float, offset: float) -> SamplingFunction:
    def f(total_length: float):
        return sample_by_length_with_offset(total_length=total_length, segment_length=segment_length, offset=offset)

    return f


# alternative name for sampling_by_length
regular = sampling_by_length


def regular_even(segment_length: float) -> SamplingFunction:
    """
    Returns a sampling function which spaces the samples equally with a segment length that is close to segment_length.
    Ensures that the number of segments is an even number.
    """

    def f(total_length: float):
        number_of_segments = (round(total_length / (2 * segment_length)) * 2)
        return sample_by_number(number_of_segments=number_of_segments)

    return f


def regular_odd(segment_length: float) -> SamplingFunction:
    """
    Returns a sampling function which spaces the samples equally with a segment length that is close to segment_length.
    Ensures that the number of segments is an odd (uneven) number.
    """

    def f(total_length: float):
        number_of_segments = (round(total_length / (2 * segment_length)) * 2) + 1
        return sample_by_number(number_of_segments=number_of_segments)

    return f
