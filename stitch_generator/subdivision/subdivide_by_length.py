import numpy as np

from stitch_generator.framework.types import SubdivisionFunction, Array1D
from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number


def subdivide_by_length(total_length: float, segment_length: float) -> Array1D:
    if np.isclose(total_length, 0) or (segment_length > total_length) or np.isclose(segment_length, 0):
        return subdivide_by_number(1)

    number_of_segments = int(round(total_length / segment_length))
    return subdivide_by_number(number_of_segments=number_of_segments)


def subdivision_by_length(segment_length: float) -> SubdivisionFunction:
    def f(total_length: float):
        return subdivide_by_length(total_length=total_length, segment_length=segment_length)

    return f


def subdivide_by_length_with_offset(total_length: float, segment_length: float, offset: float) -> Array1D:
    segment_to_length = segment_length / total_length if total_length > 0 else 0
    offset = (offset % 1) * segment_to_length

    values = subdivide_by_length(total_length=total_length, segment_length=segment_length)[:-1] + offset
    return values


def subdivision_by_length_with_offset(segment_length: float, offset: float) -> SubdivisionFunction:
    def f(total_length: float):
        return subdivide_by_length_with_offset(total_length=total_length, segment_length=segment_length, offset=offset)

    return f


# alternative name for subdivision_by_length
regular = subdivision_by_length


def regular_even(segment_length: float) -> SubdivisionFunction:
    """
    Returns a subdivision function which spaces the values equally with a segment length that is close to
    segment_length. Ensures that the number of values is an even number.
    """

    def f(total_length: float):
        number_of_segments = (round(total_length / (2 * segment_length)) * 2) + 1
        return subdivide_by_number(number_of_segments=number_of_segments)

    return f


def regular_odd(segment_length: float) -> SubdivisionFunction:
    """
    Returns a subdivision function which spaces the values equally with a segment length that is close to
    segment_length. Ensures that the number of values is an odd (uneven) number.
    """

    def f(total_length: float):
        number_of_segments = (round(total_length / (2 * segment_length)) * 2)
        return subdivide_by_number(number_of_segments=number_of_segments)

    return f
