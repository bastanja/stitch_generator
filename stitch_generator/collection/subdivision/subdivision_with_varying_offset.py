from functools import partial

from stitch_generator.collection.functions.functions_1d import linear_0_1
from stitch_generator.framework.types import Function1D, SubdivisionFunction
from stitch_generator.functions.function_modifiers import repeat, chain
from stitch_generator.functions.functions_1d import sinus, arc, linear_interpolation
from stitch_generator.subdivision.subdivide_by_fixed_length import subdivide_by_fixed_length
from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number
from stitch_generator.subdivision.subdivision_modifiers import cycle_offsets


def subdivision_with_wave_offset(segment_length: float, steps: int, function_range=(0, 1)):
    return subdivision_with_varying_offset(segment_length=segment_length, steps=steps,
                                           offset_function=to_range(sinus, function_range))


def subdivision_with_arc_offset(segment_length: float, steps: int, function_range=(0, 1)):
    return subdivision_with_varying_offset(segment_length=segment_length, steps=steps,
                                           offset_function=to_range(arc, function_range))


def subdivision_with_triangle_offset(segment_length: float, steps: int, function_range=(0, 1)):
    offset_function = to_range(repeat(2, linear_0_1, mode="reflect"), function_range)
    return subdivision_with_varying_offset(segment_length=segment_length, steps=steps, offset_function=offset_function)


def to_range(offset_function, function_range):
    return chain(offset_function, linear_interpolation(function_range[0], function_range[1]))


def subdivision_with_varying_offset(segment_length: float, steps: int, offset_function: Function1D,
                                    alignment=0.5) -> SubdivisionFunction:
    """
    Creates a subdivision function where the values are shifted by an offset each time the function is called. The
    offsets are based on 'offset_function'. This creates a pattern with the shape of the offset_function.

    Args:
        segment_length: The length of the segments between the values
        steps: The number of steps until the offset of the subdivision repeats
        offset_function: the function that defines the offset for each step
        alignment: The alignment of the subdivision pattern relative to the total length that is subdivided. Should be
                   int the range [0,1]

    Returns:
        A SubdivisionFunction
    """

    # create the offsets by number
    offsets = offset_function(subdivide_by_number(steps)[:-1])

    # create a subdivision function without the parameter 'offset'
    subdivision = partial(subdivide_by_fixed_length, segment_length=segment_length, alignment=alignment)

    # create a subdivision function which cycles through the given offset
    subdivision = cycle_offsets(subdivision, offsets)

    return subdivision
