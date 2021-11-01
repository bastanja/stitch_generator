from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import repeat, shift
from stitch_generator.functions.functions_1d import linear_interpolation


def add_gap(function, gap_offset_mm, gap_length_mm):
    mm_to_offset = linear_interpolation(0, 1, source_low=0, source_high=estimate_length(function))

    # make it circular
    result = repeat(1, function, mode='wrap')

    # shift start by the gap length and the additional offset from parameters
    shift_amount = mm_to_offset(gap_length_mm + gap_offset_mm)
    result = shift(amount=shift_amount, function=result)

    # shorten by gap length
    result = repeat(1 - (mm_to_offset(gap_length_mm)), function=result)

    return result