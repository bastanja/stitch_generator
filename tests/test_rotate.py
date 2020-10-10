import numpy as np

from stitch_generator.stitch_effects.rotate import rotate_deg, rotate


def test_rotate_deg():
    stitches = np.array(((0, 0), (10, 0)))
    rotated = rotate_deg(stitches, 90)
    assert np.allclose(rotated, np.array(((0, 0), (0, 10))))


def test_rotate():
    stitches = np.array(((0, 0), (1.0, 0), (10, 0)))
    angle = np.deg2rad(90)
    rotated = rotate(stitches, np.sin(angle), np.cos(angle))

    expected_result = np.array(((0, 0), (0, 1), (0, 10)))
    assert np.allclose(rotated, expected_result)
