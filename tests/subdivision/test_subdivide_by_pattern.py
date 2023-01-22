from typing import List

import numpy as np
import pytest

from stitch_generator.subdivision.subdivide_by_pattern import pattern_from_spaces, subdivision_by_pattern

test_values = [([2, 8], [0, 0.2, 1], True, True),
               ([2, 2], [0, 0.5], True, False),
               ([4, 6], [0.4, 1], False, True),
               ([1, 3], [0.25], False, False),
               ([1, 1, 1, 1, 1], [0, 0.2, 0.4, 0.6, 0.8, 1], True, True),
               ([2, 2, 2, 2, 2], [0, 0.2, 0.4, 0.6, 0.8, 1], True, True)]


@pytest.mark.parametrize("spaces, expected_result, with_start, with_end", test_values)
def test_pattern_from_spaces(spaces, expected_result, with_start: bool, with_end: bool):
    result = pattern_from_spaces(spaces=spaces, with_start=with_start, with_end=with_end)
    assert (np.allclose(result, expected_result))


def to_tuple(
        pattern: List[float],
        pattern_length: float,
        total_length: float,
        alignment: float,
        offset: float,
        expected_values: List[float]):
    return pattern, pattern_length, total_length, alignment, offset, expected_values


test_values = [to_tuple(pattern=[0], pattern_length=1, total_length=5, alignment=0, offset=0,
                        expected_values=[0, 0.2, 0.4, 0.6, 0.8]),
               to_tuple(pattern=[0, 0.25], pattern_length=2, total_length=10, alignment=0, offset=0,
                        expected_values=[0, 0.05, 0.2, 0.25, 0.4, 0.45, 0.6, 0.65, 0.8, 0.85]),
               to_tuple(pattern=[0, 0.25], pattern_length=2, total_length=10, alignment=0, offset=0.5,
                        expected_values=[0.1, 0.15, 0.3, 0.35, 0.5, 0.55, 0.7, 0.75, 0.9, 0.95]),
               to_tuple(pattern=[0, 0.25], pattern_length=2, total_length=5, alignment=0, offset=0.5,
                        expected_values=[0.2, 0.3, 0.6, 0.7, 1]),
               to_tuple(pattern=[0, 0.25], pattern_length=2, total_length=0, alignment=0, offset=0,
                        expected_values=[0, 1]),
               to_tuple(pattern=[0], pattern_length=0, total_length=5, alignment=0, offset=0, expected_values=[0, 1])]


@pytest.mark.parametrize("pattern, pattern_length, total_length, alignment, offset, expected_values", test_values)
def test_subdivision_by_pattern(pattern, pattern_length, total_length, alignment, offset, expected_values):
    subdivision_function = subdivision_by_pattern(pattern=pattern, pattern_length=pattern_length, alignment=alignment,
                                                  offset=offset)
    values = subdivision_function(total_length)
    assert (np.allclose(values, expected_values))
