import numpy as np

from stitch_generator.framework import Path
from stitch_generator.functions.functions_1d import constant
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.path_effects.tile_motif import tile_motif

v_motif = np.array(((0, 0), (0.5, 1), (1, 0)), dtype=float)


def line_path(origin, to, width) -> Path:
    shape, direction = line(origin, to)
    return Path(
        shape=shape,
        direction=direction,
        width=constant(width),
        stroke_alignment=constant(0.5),
    )


def test_tile_motif_on_path_shorter_than_motif():
    path = line_path(origin=(10, 0), to=(15, 0), width=6)
    stitches = tile_motif(motif=v_motif, motif_length=15)(path)
    assert stitches.shape == (3, 2)
    assert np.all(np.isfinite(stitches))
    assert np.allclose(stitches[0], (10, -3))
    assert np.allclose(stitches[-1], (15, -3))
