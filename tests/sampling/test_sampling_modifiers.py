import numpy as np
import pytest

from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.sampling.sample_by_number import sampling_by_number
from stitch_generator.sampling.sampling_modifiers import add_start, add_end, remove_end, remove_start, ensure_sample_at

sampling_functions = [
    lambda total_length: np.array([0.3, 0.5, 0.7]),  # without start and end
    lambda total_length: np.array([0, 0.5, 0.7]),  # with start
    lambda total_length: np.array([0.3, 0.5, 1]),  # with end
    regular(5),
    sampling_by_number(10)
]

lengths = [0.5, 1, 1.7, 2, 5, 10, 100, 100.5]


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
