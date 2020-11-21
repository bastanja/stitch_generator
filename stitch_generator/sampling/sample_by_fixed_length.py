from stitch_generator.functions.types import Array1D, SamplingFunction
from stitch_generator.sampling.sample import sample


def sample_by_fixed_length(total_length: float, segment_length: float, include_endpoint: bool) -> Array1D:
    return sample(total_length=total_length, segment_length=segment_length, alignment=0,
                  include_endpoint=include_endpoint, offset=0, minimal_segment_size=0)


def sampling_by_fixed_length(segment_length: float, include_endpoint: bool) -> SamplingFunction:
    def f(total_length: float):
        return sample_by_fixed_length(total_length=total_length, segment_length=segment_length,
                                include_endpoint=include_endpoint)

    return f
