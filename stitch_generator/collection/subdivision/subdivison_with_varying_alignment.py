from functools import partial

from stitch_generator.collection.functions.functions_1d import linear_0_1, positive_sine
from stitch_generator.collection.subdivision.subdivision_with_varying_offset import to_range
from stitch_generator.framework.types import Function1D, SubdivisionFunction
from stitch_generator.functions.function_modifiers import repeat
from stitch_generator.functions.functions_1d import arc
from stitch_generator.subdivision.subdivide_by_fixed_length import subdivide_by_fixed_length
from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number
from stitch_generator.subdivision.subdivision_modifiers import cycle_alignments


def subdivision_with_wave_alignment(segment_length: float, steps: int, function_range=(0, 1)):
    return subdivision_with_varying_alignment(segment_length=segment_length, steps=steps,
                                              alignment_function=to_range(positive_sine, function_range))


def subdivision_with_arc_alignment(segment_length: float, steps: int, function_range=(0, 1)):
    return subdivision_with_varying_alignment(segment_length=segment_length, steps=steps,
                                              alignment_function=to_range(arc, function_range))


def subdivision_with_triangle_alignment(segment_length: float, steps: int, function_range=(0, 1)):
    alignment_function = to_range(repeat(2, linear_0_1, mode="reflect"), function_range)
    return subdivision_with_varying_alignment(segment_length=segment_length, steps=steps,
                                              alignment_function=alignment_function)


def subdivision_with_varying_alignment(segment_length: float, steps: int, alignment_function: Function1D,
                                       offset=0) -> SubdivisionFunction:
    """
    Creates a subdivision function where the values are aligned to a new alignment value each time the function is
    called. The alignments are based on 'alignment_function'. This creates a pattern with the shape of the
    alignment_function.

    Args:
        segment_length: The length of the segments between the values
        steps: The number of steps until the alignment of the subdivision repeats
        alignment_function: the function that defines the alignment for each step
        offset: The offset of the subdivision pattern relative to the segment_length. Should be in the range [0,1]

    Returns:
        A SubdivisionFunction
    """

    # create the alignments by number
    alignments = alignment_function(subdivide_by_number(steps)[:-1])

    # create a subdivision function without the parameter 'alignment'
    subdivision = partial(subdivide_by_fixed_length, segment_length=segment_length, offset=offset)

    # create a subdivision function which cycles through the given alignment values
    subdivision = cycle_alignments(subdivision, alignments)

    return subdivision
