import numpy as np

from stitch_generator.functions.types import SamplingFunction, Array1D
from stitch_generator.sampling.sample_by_number import sample_by_number


def sample_by_length(total_length: float, segment_length: float, include_endpoint: bool) -> Array1D:
    if np.isclose(total_length, 0) or np.isclose(segment_length, 0) or segment_length > total_length:
        return sample_by_number(1, include_endpoint=include_endpoint)

    number_of_segments = int(round(total_length / segment_length))
    return sample_by_number(number_of_segments=number_of_segments, include_endpoint=include_endpoint)


def sampling_by_length(segment_length: float, include_endpoint: bool) -> SamplingFunction:
    def f(total_length: float):
        return sample_by_length(total_length=total_length, segment_length=segment_length,
                                include_endpoint=include_endpoint)

    return f


def sample_by_length_with_offset(total_length: float, segment_length: float, offset: float) -> Array1D:
    segment_to_length = segment_length / total_length if total_length > 0 else 0
    offset = (offset % 1) * segment_to_length

    samples = sample_by_length(total_length=total_length, segment_length=segment_length,
                               include_endpoint=False) + offset
    return samples


def sampling_by_length_with_offset(segment_length: float, offset: float) -> SamplingFunction:
    def f(total_length: float):
        return sample_by_length_with_offset(total_length=total_length, segment_length=segment_length, offset=offset)

    return f


def regular(segment_length: float) -> SamplingFunction:
    return sampling_by_length(segment_length, include_endpoint=True)


if __name__ == "__main__":
    test = sample_by_length_with_offset(2, 2, 0.25)
    print(test)
