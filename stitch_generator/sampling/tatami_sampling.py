import itertools
from functools import partial
from typing import Iterable

from stitch_generator.sampling.sample import sample
from stitch_generator.sampling.sampling_modifiers import free_start, free_end
from stitch_generator.utilities.types import SamplingFunction


def tatami_sampling(segment_length: float, offsets: Iterable[float], alignment: float,
                    minimal_segment_size: float = 1) -> SamplingFunction:
    offset_gen = itertools.cycle(offsets)
    sampling_function = partial(sample, segment_length=segment_length, alignment=alignment)

    def f(total_length: float):
        return sampling_function(offset=next(offset_gen), total_length=total_length)

    return free_start(minimal_segment_size, free_end(minimal_segment_size, f))
