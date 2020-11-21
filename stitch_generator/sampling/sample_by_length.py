import numpy as np

from stitch_generator.functions.types import SamplingFunction
from stitch_generator.sampling.sample_by_number import sample_by_number


def sample_by_length(total_length: float, segment_length: float, include_endpoint: bool):
    if np.isclose(total_length, 0) or np.isclose(segment_length, 0) or segment_length > total_length:
        return sample_by_number(1, include_endpoint=include_endpoint)

    number_of_segments = int(round(total_length / segment_length))
    return sample_by_number(number_of_segments=number_of_segments, include_endpoint=include_endpoint)


def sampling_by_length(segment_length: float, include_endpoint: bool) -> SamplingFunction:
    def f(total_length: float):
        return sample_by_length(total_length=total_length, segment_length=segment_length,
                                include_endpoint=include_endpoint)

    return f




