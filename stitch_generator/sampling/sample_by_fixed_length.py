from stitch_generator.sampling.sample import sample, sample_inner
from stitch_generator.utilities.types import Array1D, SamplingFunction


def sample_by_fixed_length(total_length: float, segment_length: float, include_endpoint: bool, alignment: float = 0,
                           offset: float = 0, minimal_segment_size: float = 0) -> Array1D:
    return sample(total_length=total_length, segment_length=segment_length, alignment=alignment,
                  include_endpoint=include_endpoint, offset=offset, minimal_segment_size=minimal_segment_size)


def sampling_by_fixed_length(segment_length: float, include_endpoint: bool, alignment: float = 0,
                             offset: float = 0, minimal_segment_size: float = 0) -> SamplingFunction:
    def f(total_length: float):
        return sample_by_fixed_length(total_length=total_length, segment_length=segment_length,
                                      include_endpoint=include_endpoint, alignment=alignment,
                                      offset=offset, minimal_segment_size=minimal_segment_size)

    return f


def inner_sampling_by_fixed_length(segment_length: float, alignment: float = 0,
                                   offset: float = 0, minimal_segment_size: float = 0) -> SamplingFunction:
    def f(total_length: float):
        return sample_inner(total_length=total_length, segment_length=segment_length, alignment=alignment,
                            offset=offset, minimal_segment_size=minimal_segment_size)

    return f
