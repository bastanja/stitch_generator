import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.framework.types import Array2D
from stitch_generator.functions.motif_to_path import motif_to_path


def tile_motif(motif, motif_length):
    return lambda path: tile_motif_along(path, motif, motif_length)


def tile_motif_along(path: Path, motif: Array2D, motif_length: float):
    repetitions = int(round(path.length / motif_length))
    motif_tiled = np.tile(motif, reps=(repetitions, 1))
    offsets = np.repeat(np.arange(start=0, stop=repetitions), repeats=len(motif))
    motif_tiled[:, 0] += offsets
    motif_tiled[:, 0] /= repetitions
    return motif_to_path(motif_tiled, path)
