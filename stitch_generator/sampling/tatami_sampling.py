from functools import partial
from typing import Iterable

from stitch_generator.framework.types import SamplingFunction
from stitch_generator.sampling.sample import sample
from stitch_generator.sampling.sampling_modifiers import free_start, free_end, cycle_offsets


def tatami_sampling(segment_length: float, offsets: Iterable[float], alignment: float,
                    minimal_segment_size: float = 1) -> SamplingFunction:
    sampling_function = partial(sample, segment_length=segment_length, alignment=alignment)
    return free_start(minimal_segment_size, free_end(minimal_segment_size, cycle_offsets(sampling_function, offsets)))
