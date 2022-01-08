from functools import partial

import numpy as np

from stitch_generator.functions.ensure_shape import ensure_1d_shape
from stitch_generator.sampling.sample_by_fixed_length import sample_by_fixed_length


def sampling_by_pattern(pattern,
                        pattern_length: float,
                        alignment: float,
                        offset: float):
    return partial(sample_by_pattern, pattern=pattern, pattern_length=pattern_length, alignment=alignment,
                   offset=offset)


def get_pattern_offset(relative_pattern_length: float, offset: float, alignment: float):
    # Map alignment into the range of one pattern length
    alignment = alignment % relative_pattern_length

    # Calculate the alignment position relative to one pattern length
    relative_alignment = alignment / relative_pattern_length

    # Move the pattern by offset and relative alignment
    return offset + relative_alignment


def apply_pattern_offset(pattern, offset):
    # Make sure the pattern stays in the range between 0 and 1, sort the pattern in ascending order
    return np.sort((pattern + offset) % 1)


def sample_by_pattern(total_length: float,
                      pattern_length: float,
                      pattern: list[float],
                      alignment: float,
                      offset: float):
    """
    Args:
        total_length: The total length to sample in millimeters
        pattern_length: The length of one pattern repetition in millimeters
        pattern: The sampling pattern containing sampling points in the rage from 0 to 1.
        alignment: The alignment of the start of the sampling pattern relative to the total length.
                   Values between 0 and 1.
        offset: The offset by which the pattern is shifted, relative to pattern_length

    Returns:
        The samples which subdivide the total length in segments
    """
    if np.isclose(total_length, 0):
        return ensure_1d_shape([0, 1])

    # The length of the pattern relative to the total length
    relative_pattern_length = pattern_length / total_length

    # Calculate the offset which the pattern has at the start
    effective_pattern_offset = get_pattern_offset(relative_pattern_length=relative_pattern_length,
                                                  offset=offset, alignment=alignment)

    # Apply the pattern offset
    pattern = apply_pattern_offset(np.asarray(pattern, dtype=float), effective_pattern_offset)

    # Scale the pattern relative to the total length
    pattern *= relative_pattern_length

    # Calculate start points for the pattern repetitions
    start_points = sample_by_fixed_length(total_length=total_length, segment_length=pattern_length)

    # Place one pattern repetition at each start point
    tiled_pattern = np.concatenate([pattern + p for p in start_points])

    # Cut off values above 1
    tiled_pattern = tiled_pattern[tiled_pattern <= 1]

    return tiled_pattern


def pattern_from_spaces(spaces, with_start, with_end):
    """
    Creates sample positions between 0 and 1, where the distance between the samples corresponds to the spaces.

    Args:
        spaces: distances between two neighboring samples
        with_start: If true, the result will start with sample value 0
        with_end: If true, the result will end with sample value 1

    Returns:
        Sampling positions between 0 and 1. N-1 samples for N spaces, plus one for the start and one for the end.
    """
    positions = np.cumsum(np.asarray(spaces, dtype=float))
    last = positions[-1]
    positions /= last
    if with_start:
        positions = np.concatenate([[0], positions])
    if not with_end:
        positions = positions[:-1]
    return positions
