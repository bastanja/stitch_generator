import numpy as np

from stitch_generator.stitch_effects.path_effects.meander import meander
from stitch_generator.subdivision import subdivision_by_pattern
from stitch_generator.subdivision.subdivide_by_length import regular
from tests.paths import line_path


def test_meander_without_values():
    path = line_path(origin=(10, 0), to=(40, 0), width=6)
    stitches = meander(lambda _: np.array([]), regular(3))(path)
    assert stitches.ndim == 2
    assert len(stitches) >= 2


def test_meander_with_single_value():
    path = line_path(origin=(10, 0), to=(40, 0), width=6)
    stitches = meander(lambda _: np.array([0.5]), regular(3))(path)
    # one line from the left to the right boundary
    assert np.allclose(stitches[0], (25, -3))
    assert np.allclose(stitches[-1], (25, 3))


def test_meander_on_short_path():
    path = line_path(origin=(0, 0), to=(2, 0), width=6)
    spacing_function = subdivision_by_pattern(
        pattern=(0, 0.7), pattern_length=5, alignment=0, offset=0
    )
    stitches = meander(spacing_function, regular(3))(path)
    assert stitches.ndim == 2
    assert len(stitches) >= 2
