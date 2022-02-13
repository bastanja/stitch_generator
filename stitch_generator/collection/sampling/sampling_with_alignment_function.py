from functools import partial

from stitch_generator.collection.functions.functions_1d import linear_0_1
from stitch_generator.collection.sampling.sampling_with_offset_function import to_range
from stitch_generator.framework.types import Function1D, SamplingFunction
from stitch_generator.functions.function_modifiers import repeat
from stitch_generator.functions.functions_1d import sinus, arc
from stitch_generator.sampling.sample_by_fixed_length import sample_by_fixed_length
from stitch_generator.sampling.sample_by_number import sample_by_number
from stitch_generator.sampling.sampling_modifiers import cycle_alignments


def wave_alignment_sampling(segment_length: float, steps: int, function_range=(0, 1)):
    return sampling_with_alignment_function(segment_length=segment_length, steps=steps,
                                            alignment_function=to_range(sinus, function_range))


def arc_alignment_sampling(segment_length: float, steps: int, function_range=(0, 1)):
    return sampling_with_alignment_function(segment_length=segment_length, steps=steps,
                                            alignment_function=to_range(arc, function_range))


def triangle_alignment_sampling(segment_length: float, steps: int, function_range=(0, 1)):
    alignment_function = to_range(repeat(2, linear_0_1, mode="reflect"), function_range)
    return sampling_with_alignment_function(segment_length=segment_length, steps=steps,
                                            alignment_function=alignment_function)


def sampling_with_alignment_function(segment_length: float, steps: int, alignment_function: Function1D,
                                     offset=0) -> SamplingFunction:
    """
    Creates a sampling function where the samples are aligned to a new alignment value each time the function is called.
    The alignments are based on 'alignment_function'. This creates a pattern with the shape of the alignment_function.

    Args:
        segment_length: The length of the segments between the samples
        steps: The number of offsets until the sampling repeats
        alignment_function: the function that defines the alignment for each step
        offset: The offset of the sampling pattern relative to the segment_length. Should be in the range [0,1]

    Returns:
        A SamplingFunction
    """

    # create the alignments by number
    alignments = alignment_function(sample_by_number(steps)[:-1])

    # create a sampling function without the parameter 'alignment'
    sampling_function = partial(sample_by_fixed_length, segment_length=segment_length, offset=offset)

    # create a sampling function which cycles through the given offset
    sampling_function = cycle_alignments(sampling_function, alignments)

    return sampling_function
