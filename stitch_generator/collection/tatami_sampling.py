from functools import partial

import numpy as np

from stitch_generator.framework.types import SamplingFunction
from stitch_generator.sampling.sample_by_fixed_length import sample_by_fixed_length

from stitch_generator.sampling.sample_by_number import sample_by_number
from stitch_generator.sampling.sampling_modifiers import free_start, free_end, cycle_offsets


def tatami(segment_length: float, steps: int, repetitions: int = 1, alignment=0.5,
           minimal_segment_size: float = 1) -> SamplingFunction:
    """
    Creates a sampling function where the samples are shifted by an offset each time the function is called. This
    results in a pattern with a woven look, similar to tatami mats

    Args:
        segment_length: The length of the segments between the samples
        steps: The number of offsets until the sampling repeats
        repetitions: The number of times each offset is repeated before the next offset is used
        alignment: The alignment of the sampling pattern relative to the total length tht is sampled. Should be in the
            range [0,1]
        minimal_segment_size: The minimal distance of the first sample from the start and the last sample from the end

    Returns:
        A SamplingFunction
    """

    # create the offsets by number
    offsets = sample_by_number(steps)[:-1]

    # repeat the offsets
    offsets = np.repeat(offsets, repeats=repetitions)

    # create a sampling function without the parameter 'offset'
    sampling_function = partial(sample_by_fixed_length, segment_length=segment_length, alignment=alignment)

    # create a sampling function which cycles through the given offset
    sampling_function = cycle_offsets(sampling_function, offsets)

    # keep start and end free of samples
    sampling_function = free_start(minimal_segment_size, free_end(minimal_segment_size, sampling_function))

    return sampling_function


def tatami_3_1(segment_length: float):
    return tatami(segment_length=segment_length, steps=3, repetitions=1)


def tatami_4_2(segment_length: float):
    return tatami(segment_length=segment_length, steps=4, repetitions=2)


def tatami_3_3(segment_length: float):
    return tatami(segment_length=segment_length, steps=3, repetitions=3)
