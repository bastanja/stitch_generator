from stitch_generator.sampling.sample import sample
from stitch_generator.utilities.types import Array1D, SamplingFunction


def sample_by_fixed_length(total_length: float, segment_length: float, alignment: float = 0,
                           offset: float = 0) -> Array1D:
    return sample(total_length=total_length, segment_length=segment_length, alignment=alignment, offset=offset)


def sampling_by_fixed_length(segment_length: float, alignment: float = 0, offset: float = 0) -> SamplingFunction:
    def f(total_length: float):
        return sample_by_fixed_length(total_length=total_length, segment_length=segment_length, alignment=alignment,
                                      offset=offset)

    return f
