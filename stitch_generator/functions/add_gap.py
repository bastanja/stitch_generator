from stitch_generator.framework.path import Path
from stitch_generator.framework.types import Function2D
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import repeat, shift, chain
from stitch_generator.functions.functions_1d import linear_interpolation


def add_gap_to_shape(function: Function2D, gap_offset_mm, gap_length_mm) -> Function2D:
    """
    Takes a closed shape function and adds a gap to it. This can be used e.g. for turning openings

    Args:
        function: A 2DFunction describing a closed shape, e.g. a circle
        gap_offset_mm: The distance from the shape start to the start of the gap in millimeters
        gap_length_mm: The length of the gap in millimeters

    Returns:
        A 2D function that starts after the end of the gap, goes around the shape and ends at the start of the gap
    """
    modifier = _get_modifier(estimate_length(function), gap_offset_mm, gap_length_mm)
    return modifier(function)


def add_gap_to_path(path: Path, gap_offset_mm, gap_length_mm) -> Path:
    """
    Takes a closed path and adds a gap to it. This can be used e.g. for turning openings

    Args:
        path: A Path describing a closed shape, e.g. a circle
        gap_offset_mm: The distance from the shape start to the start of the gap in millimeters
        gap_length_mm: The length of the gap in millimeters

    Returns:
        A path that starts after the end of the gap, goes around the shape and ends at the start of the gap
    """
    modifier = _get_modifier(estimate_length(path.shape), gap_offset_mm, gap_length_mm)
    return path.apply_modifier(modifier)


def _get_modifier(shape_length, gap_offset_mm, gap_length_mm):
    # create a function to convert mm into offsets between 0 and 1
    mm_to_offset = linear_interpolation(0, 1, source_low=0, source_high=shape_length)

    # create function to make the path circular
    def make_circular(f):
        return repeat(r=1, function=f, mode='wrap')

    # shift start by the gap length and the additional offset from parameters
    def apply_shift(f):
        return shift(amount=mm_to_offset(gap_length_mm + gap_offset_mm), function=f)

    # shorten by gap length
    def shorten(f):
        return repeat(r=(1 - mm_to_offset(gap_length_mm)), function=f)

    all_modifiers = chain(make_circular, chain(apply_shift, shorten))

    return all_modifiers
