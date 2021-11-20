from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import repeat, shift
from stitch_generator.functions.functions_1d import linear_interpolation
from stitch_generator.utilities.types import Function2D


def add_gap(function: Function2D, gap_offset_mm, gap_length_mm) -> Function2D:
    """
    Takes a closed shape function and adds a gap to it. This can be used e.g. for turning openings

    Args:
        function: A 2DFunction describing a closed shape, e.g. a circle
        gap_offset_mm: The distance from the shape start to the start of the gap in millimeters
        gap_length_mm: The length of the gap in millimeters

    Returns:
        A 2D function that starts after the end of the gap, goes around the shape and ends at the start of the gap
    """
    mm_to_offset = linear_interpolation(0, 1, source_low=0, source_high=estimate_length(function))

    # make it circular
    result = repeat(1, function, mode='wrap')

    # shift start by the gap length and the additional offset from parameters
    shift_amount = mm_to_offset(gap_length_mm + gap_offset_mm)
    result = shift(amount=shift_amount, function=result)

    # shorten by gap length
    result = repeat(1 - (mm_to_offset(gap_length_mm)), function=result)

    return result
