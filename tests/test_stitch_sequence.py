import numpy as np

from stitch_generator.functions.stitch_sequence import stitch_sequence_absolute


def test_stitch_sequence_absolute():
    length = 10
    stitch_length = 2
    origin = 5
    stitch_offset = 0
    min_stitch_length = 1

    sequence = stitch_sequence_absolute(length, stitch_length, min_stitch_length, origin, stitch_offset)
    assert sequence.dtype == float
    assert np.allclose(sequence, (0, 1, 3, 5, 7, 9, 10))

    stitch_offset = 1
    sequence = stitch_sequence_absolute(length, stitch_length, min_stitch_length, origin, stitch_offset)
    assert np.allclose(sequence, (0, 2, 4, 6, 8, 10))

    stitch_offset = 0.5
    sequence = stitch_sequence_absolute(length, stitch_length, min_stitch_length, origin, stitch_offset)
    assert np.allclose(sequence, (0, 1.5, 3.5, 5.5, 7.5, 10))

    stitch_offset = -0.5
    sequence = stitch_sequence_absolute(length, stitch_length, min_stitch_length, origin, stitch_offset)
    assert np.allclose(sequence, (0, 2.5, 4.5, 6.5, 8.5, 10))

    stitch_offset = 0.5
    min_stitch_length = 0.25
    sequence = stitch_sequence_absolute(length, stitch_length, min_stitch_length, origin, stitch_offset)
    assert np.allclose(sequence, (0, 1.5, 3.5, 5.5, 7.5, 9.5, 10))

    length = 2
    stitch_length = 2
    origin = 1
    stitch_offset = 0
    min_stitch_length = 1
    sequence = stitch_sequence_absolute(length, stitch_length, min_stitch_length, origin, stitch_offset)
    assert np.allclose(sequence, (0, 1, 2))

    origin = 0
    sequence = stitch_sequence_absolute(length, stitch_length, min_stitch_length, origin, stitch_offset)
    assert np.allclose(sequence, (0, 2))
