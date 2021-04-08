import itertools
from functools import partial
from typing import Iterable

from stitch_generator.sampling.sample import sample_inner
from stitch_generator.sampling.sampling_modifiers import alternate_direction, add_start_end
from stitch_generator.utilities.types import SamplingFunction


def tatami_sampling(stitch_length: float, offsets: Iterable[float], alignment: float, include_endpoint: bool,
                    include_startpoint: bool = True, minimal_segment_size: float = 0.25) -> SamplingFunction:
    offset_gen = itertools.cycle(offsets)
    sampling_function = partial(sample_inner, segment_length=stitch_length, alignment=alignment,
                                minimal_segment_size=minimal_segment_size)

    def f(total_length: float):
        return add_start_end(sampling_function(offset=next(offset_gen), total_length=total_length),
                             include_startpoint=include_startpoint, include_endpoint=include_endpoint)

    return f


def alternating_tatami_sampling(stitch_length: float, include_endpoint: bool, offsets: Iterable[float],
                                alignment: float, minimal_segment_size: float = 0.25) -> SamplingFunction:
    sampling_function = tatami_sampling(stitch_length=stitch_length, offsets=offsets, alignment=alignment,
                                        include_endpoint=True, minimal_segment_size=minimal_segment_size)
    return alternate_direction(sampling_function, include_endpoint)
