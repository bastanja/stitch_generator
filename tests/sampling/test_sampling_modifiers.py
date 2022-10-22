from functools import partial

import numpy as np
import pytest

from stitch_generator.sampling.sample_by_fixed_length import sample_by_fixed_length
from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.sampling.sample_by_number import sampling_by_number
from stitch_generator.sampling.sampling_modifiers import add_start, add_end, remove_end, remove_start, ensure_sample_at, \
    free_start, free_end, cycle_offsets, cycle_alignments, alternate_direction

sampling_functions = [
    lambda total_length: np.array([0.3, 0.5, 0.7]),  # without start and end
    lambda total_length: np.array([0, 0.5, 0.7]),  # with start
    lambda total_length: np.array([0.3, 0.5, 1]),  # with end
    regular(5),
    sampling_by_number(10),
    lambda total_length: np.array([]),  # empty
]

lengths = [0.5, 1, 1.7, 2, 5, 10, 100, 100.5]


@pytest.mark.parametrize("sampling_function", sampling_functions)
def test_alternate_direction(sampling_function):
    modified = alternate_direction(sampling_function)

    for length in lengths:
        # call sampling function once for each offset and one additional time
        collected_samples = [modified(length) for _ in range(4)]

        # check that the modified function returns the same samples in every other call
        assert (np.allclose(collected_samples[0], collected_samples[2]))
        assert (np.allclose(collected_samples[1], collected_samples[3]))


@pytest.mark.parametrize("sampling_function", sampling_functions)
def test_add_start(sampling_function):
    modified = add_start(sampling_function)

    for length in lengths:
        samples = modified(length)
        assert np.isclose(samples[0], 0)


@pytest.mark.parametrize("sampling_function", sampling_functions)
def test_add_end(sampling_function):
    modified = add_end(sampling_function)

    for length in lengths:
        samples = modified(length)
        assert np.isclose(samples[-1], 1)


@pytest.mark.parametrize("sampling_function", sampling_functions)
def test_remove_start(sampling_function):
    modified = remove_start(sampling_function)

    for length in lengths:
        samples = modified(length)
        if len(samples) > 0:
            assert not np.isclose(samples[0], 0)


@pytest.mark.parametrize("sampling_function", sampling_functions)
def test_remove_end(sampling_function):
    modified = remove_end(sampling_function)

    for length in lengths:
        samples = modified(length)
        if len(samples) > 0:
            assert not np.isclose(samples[-1], 1)


@pytest.mark.parametrize("sampling_function", sampling_functions)
def test_ensure_sample_at(sampling_function):
    sample_position = 0.45
    modified = ensure_sample_at(sampling_function, sample_position)

    for length in lengths:
        samples = modified(length)
        if len(samples) > 1:
            delta = np.abs(samples - sample_position)
            nearest_index = np.argmin(delta)
            assert np.isclose(samples[nearest_index], sample_position)


@pytest.mark.parametrize("sampling_function", sampling_functions)
def test_free_start(sampling_function):
    free_start_length = 5
    modified = free_start(start_length=free_start_length, sampling_function=sampling_function)

    for length in lengths:
        samples = modified(length)
        lower_bound = free_start_length / length
        if len(samples) > 1:
            assert (np.alltrue(samples >= lower_bound))


@pytest.mark.parametrize("sampling_function", sampling_functions)
def test_free_end(sampling_function):
    free_end_length = 3
    modified = free_end(end_length=free_end_length, sampling_function=sampling_function)

    for length in lengths:
        samples = modified(length)
        upper_bound = 1 - (free_end_length / length)
        if len(samples) > 1:
            assert (np.alltrue(samples <= upper_bound))


def test_cycle_offsets():
    partial_sample_function = partial(sample_by_fixed_length, segment_length=1, alignment=0)

    offsets = [0, 0.3, 0.4]
    modified = cycle_offsets(partial_sample_function, offsets=offsets)

    for length in lengths:
        repetitions = len(offsets) + 1
        # call sampling function once for each offset and one additional time
        collected_samples = [modified(length) for _ in range(repetitions)]

        # check that first and last samples are equal
        assert (np.allclose(collected_samples[0], collected_samples[-1]))

        # check that subsequent samples are not equal
        for current, successor in zip(collected_samples, collected_samples[1:]):
            assert (not np.allclose(current, successor))


def test_cycle_alignments():
    partial_sample_function = partial(sample_by_fixed_length, segment_length=1, offset=0)

    alignments = [0, 0.3, 0.4]
    modified = cycle_alignments(partial_sample_function, alignments=alignments)

    for length in lengths:
        repetitions = len(alignments) + 1
        # call sampling function once for each alignment and one additional time
        collected_samples = [modified(length) for _ in range(repetitions)]

        # check that first and last samples are equal
        assert (np.allclose(collected_samples[0], collected_samples[-1]))
