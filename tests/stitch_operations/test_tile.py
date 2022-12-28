import numpy as np

from stitch_generator.stitch_operations.tile import tile_x, tile_y


def test_tile_x():
    stitches = np.array(((0, 0), (10, 0), (0, 10), (10, 10)))
    length = len(stitches)
    spacing = 20
    result = tile_x(stitches, spacing=spacing, repetitions=3)

    assert np.allclose(stitches, result[0: length])
    assert np.allclose(stitches + (spacing, 0), result[length: length * 2])
    assert np.allclose(stitches + (spacing * 2, 0), result[length * 2:])


def test_tile_y():
    stitches = np.array(((0, 0), (0, 10), (10, 0), (10, 10)))
    length = len(stitches)
    spacing = 10
    result = tile_y(stitches, spacing=spacing, repetitions=3)

    assert np.allclose(stitches, result[0: length])
    assert np.allclose(stitches + (0, spacing), result[length: length * 2])
    assert np.allclose(stitches + (0, spacing * 2), result[length * 2:])
