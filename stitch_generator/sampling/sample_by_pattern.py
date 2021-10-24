from functools import partial

import math
import numpy as np

from stitch_generator.functions.ensure_shape import ensure_1d_shape


def sampling_by_pattern(pattern,
                        alignment: float,
                        offset: float):
    return partial(sample_by_pattern, pattern=pattern, alignment=alignment, offset=offset)


def sample_by_pattern(total_length: float,
                      pattern: list[float],
                      alignment: float,
                      offset: float):
    """

    Args:
        total_length: The total length to sample in millimeters
        pattern: The sampling pattern in millimeters
        alignment: The alignment of the sampling pattern relative to the total length. Values between 0 and 1.
        offset: The offset by which the pattern is shifted in millimeters

    Returns:
        The samples which subdivide the total length in segments

    """
    if np.isclose(total_length, 0):
        return ensure_1d_shape([0, 1])

    pattern = np.asarray(pattern, dtype=float)
    pattern_length = np.sum(pattern)
    relative_pattern_length = pattern_length / total_length
    offset = offset / total_length

    pattern /= total_length

    repetitions = math.ceil(1 / relative_pattern_length) + 1

    tiled_pattern = np.tile(pattern, repetitions)

    offset = (offset % relative_pattern_length)

    alignment_to_offset = alignment % relative_pattern_length
    offset += alignment_to_offset

    tiled_pattern = np.cumsum(tiled_pattern) + offset

    tiled_pattern = tiled_pattern[0 <= tiled_pattern]
    tiled_pattern = tiled_pattern[tiled_pattern <= 1]

    return tiled_pattern
