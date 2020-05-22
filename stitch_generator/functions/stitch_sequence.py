import numpy as np


def stitch_sequence(length, stitch_length, min_stitch_length, origin_relative_to_length,
                    stitch_offset_relative_to_stitch_length):
    if length < min_stitch_length:
        return np.array((0.0,length))
    origin = length * origin_relative_to_length
    stitch_offset = stitch_offset_relative_to_stitch_length * stitch_length
    sequence = stitch_sequence_absolute(length, stitch_length, min_stitch_length, origin, stitch_offset)
    sequence /= length
    return sequence


def stitch_sequence_absolute(length, stitch_length, min_stitch_length, origin, stitch_offset):
    stitch_reference = origin + stitch_offset
    min_reference = min_stitch_length
    max_reference = length - min_stitch_length

    segments_before_stitch_reference = int((stitch_reference - min_reference) / stitch_length)

    first_stitch = stitch_reference - stitch_length * segments_before_stitch_reference
    while first_stitch < min_reference:
        first_stitch += stitch_length
    while first_stitch > max_reference:
        first_stitch -= stitch_length
    if first_stitch < min_reference:
        return np.array((0.0, length))

    length_reference = max_reference - first_stitch
    segments = int(length_reference / stitch_length)

    stitch_positions = np.zeros((segments + 3))
    stitch_positions[-1] = length
    stitch_positions[1:-1] = [first_stitch + i * stitch_length for i in range(segments + 1)]
    return stitch_positions
