import numpy as np

from stitch_generator.framework.types import Array1D, SamplingFunction
from stitch_generator.sampling.alignment_to_offset import alignment_to_offset
from stitch_generator.sampling.sample_by_number import sample_by_number


def sample_by_fixed_length(total_length: float,
                           segment_length: float,
                           alignment: float = 0,
                           offset: float = 0) -> Array1D:
    if total_length == 0 or segment_length == 0:
        return sample_by_number(1)
    step_size = segment_length / total_length
    step_offset = alignment_to_offset(step_size, offset, alignment) * step_size
    return np.arange(start=step_offset, step=step_size, stop=1)


def sampling_by_fixed_length(segment_length: float, alignment: float = 0, offset: float = 0) -> SamplingFunction:
    def f(total_length: float):
        return sample_by_fixed_length(total_length=total_length, segment_length=segment_length, alignment=alignment,
                                      offset=offset)

    return f
