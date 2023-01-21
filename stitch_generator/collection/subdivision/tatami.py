from functools import partial

import numpy as np

from stitch_generator.framework.types import SubdivisionFunction
from stitch_generator.subdivision.subdivide_by_fixed_length import subdivide_by_fixed_length
from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number
from stitch_generator.subdivision.subdivision_modifiers import free_start, free_end, cycle_offsets


def tatami(segment_length: float, steps: int, repetitions: int = 1, alignment=0.5,
           minimal_segment_size: float = 1) -> SubdivisionFunction:
    """
    Creates a subdivision function where the values are shifted by an offset each time the function is called. This
    results in a pattern with a woven look, similar to tatami mats

    Args:
        segment_length: The length of the segments between the values
        steps: The number of offsets until the subdivision repeats
        repetitions: The number of times each offset is repeated before the next offset is used
        alignment: The alignment of the subdivision pattern relative to the total length that is subdivided. Should be
                   in the range [0,1]
        minimal_segment_size: The minimal distance of the first value from the start and the last value from the end

    Returns:
        A SubdivisionFunction
    """

    # create the offsets by number
    offsets = subdivide_by_number(steps)[:-1]

    # repeat the offsets
    offsets = np.repeat(offsets, repeats=repetitions)

    # create a subdivision function without the parameter 'offset'
    subdivision = partial(subdivide_by_fixed_length, segment_length=segment_length, alignment=alignment)

    # create a subdivision function which cycles through the given offset
    subdivision = cycle_offsets(subdivision, offsets)

    # keep start and end free of values
    subdivision = free_start(minimal_segment_size, free_end(minimal_segment_size, subdivision))

    return subdivision


def tatami_3_1(segment_length: float):
    return tatami(segment_length=segment_length, steps=3, repetitions=1)


def tatami_4_2(segment_length: float):
    return tatami(segment_length=segment_length, steps=4, repetitions=2)


def tatami_3_3(segment_length: float):
    return tatami(segment_length=segment_length, steps=3, repetitions=3)
