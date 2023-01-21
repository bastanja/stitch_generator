from functools import partial

import numpy as np
import pytest

from stitch_generator.subdivision.subdivide_by_fixed_length import subdivide_by_fixed_length
from stitch_generator.subdivision.subdivide_by_length import regular
from stitch_generator.subdivision.subdivide_by_number import subdivision_by_number
from stitch_generator.subdivision.subdivision_modifiers import add_start, add_end, remove_end, remove_start, \
    ensure_value_at, free_start, free_end, cycle_offsets, cycle_alignments, alternate_direction

subdivision_functions = [
    lambda total_length: np.array([0.3, 0.5, 0.7]),  # without start and end
    lambda total_length: np.array([0, 0.5, 0.7]),  # with start
    lambda total_length: np.array([0.3, 0.5, 1]),  # with end
    regular(5),
    subdivision_by_number(10),
    lambda total_length: np.array([]),  # empty
]

lengths = [0.5, 1, 1.7, 2, 5, 10, 100, 100.5]


@pytest.mark.parametrize("subdivision_function", subdivision_functions)
def test_alternate_direction(subdivision_function):
    modified = alternate_direction(subdivision_function)

    for length in lengths:
        # call subdivision function once for each offset and one additional time
        collected_values = [modified(length) for _ in range(4)]

        # check that the modified function returns the same values in every other call
        assert (np.allclose(collected_values[0], collected_values[2]))
        assert (np.allclose(collected_values[1], collected_values[3]))


@pytest.mark.parametrize("subdivision_function", subdivision_functions)
def test_add_start(subdivision_function):
    modified = add_start(subdivision_function)

    for length in lengths:
        values = modified(length)
        assert np.isclose(values[0], 0)


@pytest.mark.parametrize("subdivision_function", subdivision_functions)
def test_add_end(subdivision_function):
    modified = add_end(subdivision_function)

    for length in lengths:
        values = modified(length)
        assert np.isclose(values[-1], 1)


@pytest.mark.parametrize("subdivision_function", subdivision_functions)
def test_remove_start(subdivision_function):
    modified = remove_start(subdivision_function)

    for length in lengths:
        values = modified(length)
        if len(values) > 0:
            assert not np.isclose(values[0], 0)


@pytest.mark.parametrize("subdivision_function", subdivision_functions)
def test_remove_end(subdivision_function):
    modified = remove_end(subdivision_function)

    for length in lengths:
        values = modified(length)
        if len(values) > 0:
            assert not np.isclose(values[-1], 1)


@pytest.mark.parametrize("subdivision_function", subdivision_functions)
def test_ensure_value_at(subdivision_function):
    value_position = 0.45
    modified = ensure_value_at(subdivision_function, value_position)

    for length in lengths:
        values = modified(length)
        if len(values) > 1:
            delta = np.abs(values - value_position)
            nearest_index = np.argmin(delta)
            assert np.isclose(values[nearest_index], value_position)


@pytest.mark.parametrize("subdivision_function", subdivision_functions)
def test_free_start(subdivision_function):
    free_start_length = 5
    modified = free_start(start_length=free_start_length, subdivision_function=subdivision_function)

    for length in lengths:
        values = modified(length)
        lower_bound = free_start_length / length
        if len(values) > 1:
            assert (np.alltrue(values >= lower_bound))


@pytest.mark.parametrize("subdivision_function", subdivision_functions)
def test_free_end(subdivision_function):
    free_end_length = 3
    modified = free_end(end_length=free_end_length, subdivision_function=subdivision_function)

    for length in lengths:
        values = modified(length)
        upper_bound = 1 - (free_end_length / length)
        if len(values) > 1:
            assert (np.alltrue(values <= upper_bound))


def test_cycle_offsets():
    partial_value_function = partial(subdivide_by_fixed_length, segment_length=1, alignment=0)

    offsets = [0, 0.3, 0.4]
    modified = cycle_offsets(partial_value_function, offsets=offsets)

    for length in lengths:
        repetitions = len(offsets) + 1
        # call subdivision function once for each offset and one additional time
        collected_values = [modified(length) for _ in range(repetitions)]

        # check that first and last values are equal
        assert (np.allclose(collected_values[0], collected_values[-1]))

        # check that subsequent values are not equal
        for current, successor in zip(collected_values, collected_values[1:]):
            assert (not np.allclose(current, successor))


def test_cycle_alignments():
    partial_value_function = partial(subdivide_by_fixed_length, segment_length=1, offset=0)

    alignments = [0, 0.3, 0.4]
    modified = cycle_alignments(partial_value_function, alignments=alignments)

    for length in lengths:
        repetitions = len(alignments) + 1
        # call subdivision function once for each alignment and one additional time
        collected_values = [modified(length) for _ in range(repetitions)]

        # check that first and last values are equal
        assert (np.allclose(collected_values[0], collected_values[-1]))
