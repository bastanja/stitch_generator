from functools import partial
from typing import List

import numpy as np

from stitch_generator.subdivision.alignment_to_offset import alignment_to_offset
from stitch_generator.subdivision.subdivide_by_fixed_length import subdivide_by_fixed_length
from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number


def subdivision_by_pattern(pattern,
                           pattern_length: float,
                           alignment: float,
                           offset: float):
    return partial(subdivide_by_pattern, pattern=pattern, pattern_length=pattern_length, alignment=alignment,
                   offset=offset)


def subdivide_by_pattern(total_length: float,
                         pattern_length: float,
                         pattern: List[float],
                         alignment: float,
                         offset: float):
    """
    Args:
        total_length: The total length to subdivide
        pattern_length: The length of one pattern repetition
        pattern: The subdivision pattern containing values in the rage from 0 to 1
        alignment: The alignment of the start of the subdivision pattern relative to the total length.
                   Values between 0 and 1.
        offset: The offset by which the pattern is shifted, relative to pattern_length

    Returns:
        The values which subdivide the total length in segments
    """
    if np.isclose(total_length, 0) or np.isclose(pattern_length, 0):
        return subdivide_by_number(1)

    # The length of the pattern relative to the total length
    relative_pattern_length = pattern_length / total_length

    # Calculate the offset which the pattern has at the start
    effective_pattern_offset = alignment_to_offset(relative_segment_length=relative_pattern_length,
                                                   offset=offset, alignment=alignment)

    # Apply the pattern offset
    pattern = _apply_pattern_offset(np.asarray(pattern, dtype=float), effective_pattern_offset)

    # Scale the pattern relative to the total length
    pattern *= relative_pattern_length

    # Calculate start points for the pattern repetitions
    start_points = subdivide_by_fixed_length(total_length=total_length, segment_length=pattern_length)

    # Place one pattern repetition at each start point
    tiled_pattern = np.concatenate([pattern + p for p in start_points])

    # Cut off values above 1
    tiled_pattern = tiled_pattern[tiled_pattern <= 1]

    return tiled_pattern


def pattern_from_spaces(spaces, with_start, with_end):
    """
    Creates subdivision values between 0 and 1, where the distance between the values corresponds to the spaces.

    Args:
        spaces: distances between two neighboring subdivision values
        with_start: If true, the result contains the start value 0
        with_end: If true, the result contains the end value 1

    Returns:
        Values between 0 and 1. N-1 values for N spaces, plus one for the start and one for the end.
    """
    positions = np.cumsum(np.asarray(spaces, dtype=float))
    last = positions[-1]
    positions /= last
    if with_start:
        positions = np.concatenate([[0], positions])
    if not with_end:
        positions = positions[:-1]
    return positions


def _apply_pattern_offset(pattern, offset):
    # Make sure the pattern stays in the range between 0 and 1, sort the pattern in ascending order
    return np.sort((pattern + offset) % 1)
