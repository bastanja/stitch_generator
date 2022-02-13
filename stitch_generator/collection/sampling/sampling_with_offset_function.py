from functools import partial

from stitch_generator.collection.functions.functions_1d import linear_0_1
from stitch_generator.framework.types import Function1D, SamplingFunction
from stitch_generator.functions.function_modifiers import repeat, combine
from stitch_generator.functions.functions_1d import sinus, arc, linear_interpolation
from stitch_generator.sampling.sample_by_fixed_length import sample_by_fixed_length
from stitch_generator.sampling.sample_by_number import sample_by_number
from stitch_generator.sampling.sampling_modifiers import cycle_offsets


def wave_offset_sampling(segment_length: float, steps: int, function_range=(0, 1)):
    return sampling_with_offset_function(segment_length=segment_length, steps=steps,
                                         offset_function=to_range(sinus, function_range))


def arc_offset_sampling(segment_length: float, steps: int, function_range=(0, 1)):
    return sampling_with_offset_function(segment_length=segment_length, steps=steps,
                                         offset_function=to_range(arc, function_range))


def triangle_offset_sampling(segment_length: float, steps: int, function_range=(0, 1)):
    offset_function = to_range(repeat(2, linear_0_1, mode="reflect"), function_range)
    return sampling_with_offset_function(segment_length=segment_length, steps=steps, offset_function=offset_function)


def to_range(offset_function, function_range):
    return combine(offset_function, linear_interpolation(function_range[0], function_range[1]))


def sampling_with_offset_function(segment_length: float, steps: int, offset_function: Function1D,
                                  alignment=0.5) -> SamplingFunction:
    """
    Creates a sampling function where the samples are shifted by an offset each time the function is called. The offsets
    are based on 'offset_function'. This creates a pattern with the shape of the offset_function.

    Args:
        segment_length: The length of the segments between the samples
        steps: The number of offsets until the sampling repeats
        offset_function: the function that defines the offset for each step
        alignment: The alignment of the sampling pattern relative to the total length that is sampled. Should be in the
            range [0,1]

    Returns:
        A SamplingFunction
    """

    # create the offsets by number
    offsets = offset_function(sample_by_number(steps)[:-1])

    # create a sampling function without the parameter 'offset'
    sampling_function = partial(sample_by_fixed_length, segment_length=segment_length, alignment=alignment)

    # create a sampling function which cycles through the given offset
    sampling_function = cycle_offsets(sampling_function, offsets)

    return sampling_function
