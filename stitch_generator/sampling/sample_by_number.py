import numpy as np

from stitch_generator.utilities.types import SamplingFunction, Array1D


def sample_by_number(number_of_segments: int, include_endpoint: bool) -> Array1D:
    return linspace(start=0, stop=1, number_of_segments=number_of_segments, include_endpoint=include_endpoint)


def sampling_by_number(number_of_segments: int, include_endpoint: bool) -> SamplingFunction:
    def f(total_length: float):
        return sample_by_number(number_of_segments=number_of_segments, include_endpoint=include_endpoint)

    return f


def linspace(start: float, stop: float, number_of_segments: int, include_endpoint: bool) -> Array1D:
    number_of_samples = number_of_segments + 1 if include_endpoint else number_of_segments
    return np.linspace(start, stop, num=number_of_samples, endpoint=include_endpoint)
