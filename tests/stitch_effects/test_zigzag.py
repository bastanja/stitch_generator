import numpy as np

from stitch_generator.stitch_effects.path_effects.zigzag import double_zigzag, zigzag
from tests.paths import line_path


def no_values(_):
    return np.array([])


def single_value(_):
    return np.array([0.5])


def test_zigzag_with_fewer_than_two_values():
    path = line_path(origin=(10, 0), to=(40, 0), width=6)
    for spacing_function in (no_values, single_value):
        stitches = zigzag(spacing_function)(path)
        # zigzag once from the start on the left to the end on the right
        assert np.allclose(stitches, ((10, -3), (40, 3)))

        assert len(double_zigzag(spacing_function)(path)) >= 2
