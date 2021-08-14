import itertools
from functools import partial
from typing import Iterable

from stitch_generator.sampling.sample import sample
from stitch_generator.sampling.sampling_modifiers import alternate_direction
from stitch_generator.utilities.types import SamplingFunction


def tatami_sampling(segment_length: float, offsets: Iterable[float], alignment: float,
                    minimal_segment_size: float = 0.25) -> SamplingFunction:
    offset_gen = itertools.cycle(offsets)
    sampling_function = partial(sample, segment_length=segment_length, alignment=alignment,
                                minimal_segment_size=minimal_segment_size)

    def f(total_length: float):
        return sampling_function(offset=next(offset_gen), total_length=total_length)

    return f


def alternating_tatami_sampling(segment_length: float, offsets: Iterable[float],
                                alignment: float, minimal_segment_size: float = 0.25) -> SamplingFunction:
    sampling_function = tatami_sampling(segment_length=segment_length, offsets=offsets, alignment=alignment,
                                        minimal_segment_size=minimal_segment_size)
    return alternate_direction(sampling_function)
