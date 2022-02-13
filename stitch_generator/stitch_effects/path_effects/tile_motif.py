from stitch_generator.framework.path import Path
from stitch_generator.framework.types import Array2D
from stitch_generator.stitch_effects.utilities.motif_to_path import motif_to_path
from stitch_generator.stitch_operations.tile import tile_x


def tile_motif(motif, motif_length):
    return lambda path: tile_motif_along(path, motif, motif_length)


def tile_motif_along(path: Path, motif: Array2D, motif_length: float):
    repetitions = int(round(path.length / motif_length))
    motif_tiled = tile_x(motif=motif, spacing=1, repetitions=repetitions)
    motif_tiled[:, 0] /= repetitions
    return motif_to_path(motif_tiled, path)
