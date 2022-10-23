import numpy as np

from stitch_generator.framework.types import SamplingFunction, Array1D


def sample_by_number(number_of_segments: int) -> Array1D:
    return np.linspace(0, 1, num=number_of_segments + 1, endpoint=True)


def sampling_by_number(number_of_segments: int) -> SamplingFunction:
    def f(total_length: float):
        return sample_by_number(number_of_segments=number_of_segments)

    return f
