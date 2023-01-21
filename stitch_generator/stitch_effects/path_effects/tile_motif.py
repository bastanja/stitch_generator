import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import Array2D
from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number
from stitch_generator.stitch_effects.utilities.motif_to_path import motif_to_path
from stitch_generator.stitch_operations.tile import tile_x


def tile_motif(motif, motif_length) -> StitchEffect:
    return lambda path: tile_motif_along(path, motif, motif_length)


def tile_motif_along(path: Path, motif: Array2D, motif_length: float):
    # if the shape has no length, return start and end point
    if np.isclose(path.length, 0):
        return path.shape(subdivide_by_number(1))

    # check how many repetitions of the motif fit on the path
    repetitions = int(round(path.length / motif_length))

    # repeat the motif
    motif_tiled = tile_x(motif=motif, spacing=1, repetitions=repetitions)
    motif_tiled[:, 0] /= repetitions

    # place it on the path
    stitches = motif_to_path(motif_tiled, path)
    return stitches
