import numpy as np

from stitch_generator.stitch_effects.path_effects.satin import (
    double_satin,
    satin,
    simple_satin,
)
from stitch_generator.subdivision.subdivide_by_length import regular
from tests.paths import line_path


def count_duplicates(stitches):
    return np.sum(np.all(np.isclose(stitches[1:], stitches[:-1]), axis=1))


def test_satin_has_no_duplicate_stitches():
    path = line_path(origin=(10, 0), to=(40, 0), width=6)

    stitches = simple_satin(spacing=3, stitch_length=3)(path)
    assert count_duplicates(stitches) == 0
    assert np.allclose(stitches[0], (10, -3))

    stitches = double_satin(regular(3), regular(3))(path)
    assert count_duplicates(stitches) == 0
    # double satin ends where it started
    assert np.allclose(stitches[0], stitches[-1])


def test_satin_with_fewer_than_two_values():
    path = line_path(origin=(10, 0), to=(40, 0), width=6)
    for spacing_function in (lambda _: np.array([]), lambda _: np.array([0.5])):
        assert len(satin(spacing_function, regular(3))(path)) >= 2
        assert len(double_satin(spacing_function, regular(3))(path)) >= 2
