import itertools
from functools import partial
from typing import Iterable

from stitch_generator.functions.types import SamplingFunction
from stitch_generator.sampling.sample import sample
from stitch_generator.sampling.sampling_modifiers import alternate_direction


def tatami_sampling(stitch_length: float, include_endpoint: bool, offsets: Iterable[float], alignment: float,
                    minimal_segment_size: float = 0.25) -> SamplingFunction:
    offset_gen = itertools.cycle(offsets)
    sampling_function = partial(sample, segment_length=stitch_length, alignment=alignment,
                                include_endpoint=include_endpoint, minimal_segment_size=minimal_segment_size)

    def f(total_length: float):
        return sampling_function(offset=next(offset_gen), total_length=total_length)

    return f


def alternating_tatami_sampling(stitch_length: float, include_endpoint: bool, offsets: Iterable[float],
                                alignment: float, minimal_segment_size: float = 0.25) -> SamplingFunction:
    sampling_function = tatami_sampling(stitch_length=stitch_length, offsets=offsets, alignment=alignment,
                                        include_endpoint=True, minimal_segment_size=minimal_segment_size)
    return alternate_direction(sampling_function, include_endpoint)
