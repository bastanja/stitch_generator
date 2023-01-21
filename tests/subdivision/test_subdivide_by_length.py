from itertools import product

import numpy as np
import pytest

from stitch_generator.subdivision.subdivide_by_length import subdivide_by_length, subdivision_by_length_with_offset, \
    regular_even, \
    regular_odd

test_values = [
    # test where segments fit into length exactly
    (10, 2, 5), (12, 2, 6),
    # test with half segment
    (10.49, 2, 5), (11, 2, 6), (11.01, 2, 6),
    # test with segment length which is larger than the total length
    (5, 10, 1)
]


@pytest.mark.parametrize("total_length, segment_length, expected_segments", test_values)
def test_subdivide_by_length(total_length, segment_length, expected_segments):
    """ Test that subdivision returns equally spaced values of the expected length """
    with_endpoint = subdivide_by_length(total_length, segment_length)

    reference = [1 / expected_segments * i for i in range(expected_segments + 1)]

    assert len(with_endpoint) == expected_segments + 1
    assert np.allclose(with_endpoint, reference)


@pytest.mark.parametrize("total_length", [10, 1, 0])
def test_subdivide_by_length_segment_zero(total_length):
    """ Test subdivision with a segment length of zero """
    assert np.allclose(subdivide_by_length(total_length=total_length, segment_length=0), [0, 1])


@pytest.mark.parametrize("segment_length", [10, 1, 0])
def test_subdivide_by_length_total_zero(segment_length):
    """ Test subdivision with a total length of zero """
    assert np.allclose(
        subdivide_by_length(total_length=0, segment_length=segment_length), [0, 1])


def test_subdivide_by_length_with_offset():
    # offset of a half segment length
    subdivision = subdivision_by_length_with_offset(segment_length=1, offset=0.5)
    values = subdivision(5)
    expected_values = np.array((0.5, 1.5, 2.5, 3.5, 4.5)) / 5
    assert (np.allclose(values, expected_values))

    # offset of a quarter segment length
    subdivision = subdivision_by_length_with_offset(segment_length=1, offset=0.25)
    values = subdivision(5)
    expected_values = np.array((0.25, 1.25, 2.25, 3.25, 4.25)) / 5
    assert (np.allclose(values, expected_values))

    # negative offset
    subdivision = subdivision_by_length_with_offset(segment_length=1, offset=-0.5)
    values = subdivision(5)
    expected_values = np.array((0.5, 1.5, 2.5, 3.5, 4.5)) / 5
    assert (np.allclose(values, expected_values))

    # offset above 1
    subdivision = subdivision_by_length_with_offset(segment_length=1, offset=2.2)
    values = subdivision(3)
    expected_values = np.array((0.2, 1.2, 2.2)) / 3
    assert (np.allclose(values, expected_values))

    # segment length longer than total length
    subdivision = subdivision_by_length_with_offset(segment_length=10, offset=0.1)
    values = subdivision(5)
    expected_values = np.array((1)) / 5
    assert (np.allclose(values, expected_values))


segment_lengths = [0.01, 1, 2, 10]
total_lengths = [0.5, 1, 5.5, 10, 99]
test_values = list(product(total_lengths, segment_lengths))


@pytest.mark.parametrize("total_length, segment_length", test_values)
def test_regular_even(total_length, segment_length):
    subdivision_function = regular_even(segment_length=segment_length)
    values = subdivision_function(total_length)
    assert len(values) % 2 == 0


@pytest.mark.parametrize("total_length, segment_length", test_values)
def test_regular_odd(total_length, segment_length):
    subdivision_function = regular_odd(segment_length=segment_length)
    values = subdivision_function(total_length)
    assert len(values) % 2 == 1
