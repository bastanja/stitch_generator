from functools import partial

from stitch_generator.framework.types import Function1D, SamplingFunction
from stitch_generator.functions.function_sequence import function_sequence
from stitch_generator.functions.functions_1d import sinus, arc, linear_interpolation
from stitch_generator.sampling.sample import sample
from stitch_generator.sampling.sampling_modifiers import cycle_offsets


def wave_sampling(segment_length: float, steps: int):
    return sampling_with_offset_function(segment_length=segment_length, steps=steps, offset_function=sinus)


def arc_sampling(segment_length: float, steps: int):
    return sampling_with_offset_function(segment_length=segment_length, steps=steps, offset_function=arc)


def triangle_sampling(segment_length: float, steps: int):
    offset_function = function_sequence((linear_interpolation(0, 1), linear_interpolation(0, 1)), (1, 1))
    return sampling_with_offset_function(segment_length=segment_length, steps=steps, offset_function=offset_function)


def sampling_with_offset_function(segment_length: float, steps: int, offset_function: Function1D,
                                  alignment=0.5) -> SamplingFunction:
    """
    Creates a sampling function where the samples are shifted by an offset each time the function is called. The offsets
    are based on 'offset_function'. This creates a pattern with the shape of the offset_function.

    Args:
        segment_length: The length of the segments between the samples
        steps: The number of offsets until the sampling repeats
        offset_function: the function that defines the offset for each step
        alignment: The alignment of the sampling pattern relative to the total length tht is sampled. Should be in the
            range [0,1]

    Returns:
        A SamplingFunction
    """

    # create the offsets by number
    offsets = offset_function(steps)[:-1]

    # create a sampling function without the parameter 'offset'
    sampling_function = partial(sample, segment_length=segment_length, alignment=alignment)

    # create a sampling function which cycles through the given offset
    sampling_function = cycle_offsets(sampling_function, offsets)

    return sampling_function
