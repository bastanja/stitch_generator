import numpy as np

from stitch_generator.stitch_operations.rotate import rotate_by_degrees, rotate_by_sin_cos, rotate_90, rotate_180, \
    rotate_270


def test_rotate_deg():
    stitches = np.array(((0, 0), (10, 0)))
    rotated = rotate_by_degrees(stitches, 90)
    assert np.allclose(rotated, np.array(((0, 0), (0, 10))))


def test_rotate_90():
    stitches = np.array(((0, 0), (10, 0)))
    rotated = rotate_90(stitches)
    assert np.allclose(rotated, np.array(((0, 0), (0, 10))))


def test_rotate_180():
    stitches = np.array(((0, 0), (10, 0)))
    rotated = rotate_180(stitches)
    assert np.allclose(rotated, np.array(((0, 0), (-10, 0))))


def test_rotate_270():
    stitches = np.array(((0, 0), (10, 0)))
    rotated = rotate_270(stitches)
    assert np.allclose(rotated, np.array(((0, 0), (0, -10))))


def test_rotate():
    stitches = np.array(((0, 0), (1.0, 0), (10, 0)))
    angle = np.deg2rad(90)
    rotated = rotate_by_sin_cos(stitches, np.sin(angle), np.cos(angle))

    expected_result = np.array(((0, 0), (0, 1), (0, 10)))
    assert np.allclose(rotated, expected_result)
