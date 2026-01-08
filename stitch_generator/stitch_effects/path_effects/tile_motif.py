import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import Array2D, Coordinates
from stitch_generator.functions.estimate_length import estimate_length
from ..utilities.motif_to_path import motif_to_path
from stitch_generator.stitch_operations.tile import tile_x
from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number


def tile_motif(motif: Array2D, motif_length: float) -> StitchEffect:
    """Creates stitch effect where a motif is tiled along a path.

    Repeats a motif along a path and transforms it to fit into the boundaries of the path.

    The stitch coordinates of the motif should be in the range [0;1]. Y-coordinate 0 is placed
    at the left border of the path, Y-coordinate 1 is placed at the right border of the path.
    The motif is tiled in the x-direction. The parameter motif_length and the length of the
    path define how often the motif is repeated along the path.

    Args:
        motif: Array of 2D coordinates representing the motif. Coordinates should be in
            range [0;1] with Y=0 at left border and Y=1 at right border.
        motif_length: The length of one motif repetition along the path.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.

    Example:
        ```python
        from stitch_generator.collection.motifs.square_spiral import square_spiral
        from stitch_generator.stitch_effects.path_effects.tile_motif import tile_motif

        # create motif for tiling
        spiral_level = 5
        motif_scale = (1, spiral_level / (spiral_level - 1))  # make it square
        motif_translation = (0.5, 0.5)  # move it into the range [0,1] in x and y direction
        motif = square_spiral(level=spiral_level,
                              step_size=(1 / spiral_level)) * motif_scale + motif_translation

        # create stitch effect
        effect = tile_motif(motif=motif, motif_length=15)
        stitches = effect(path)
        ```
    """
    return lambda path: tile_motif_along(path, motif, motif_length)


def tile_motif_along(path: Path, motif: Array2D, motif_length: float) -> Coordinates:
    """Creates tiled motif stitches along a path.

    Args:
        path: The path to create tiled motif stitches along.
        motif: Array of 2D coordinates representing the motif. Coordinates should be in
            range [0;1] with Y=0 at left border and Y=1 at right border.
        motif_length: The length of one motif repetition along the path.

    Returns:
        Coordinates representing the tiled motif stitches.
    """
    # if the shape has no length, return start and end point
    path_length = estimate_length(path.shape)
    if np.isclose(path_length, 0):
        return path.shape(subdivide_by_number(1))

    # check how many repetitions of the motif fit on the path
    repetitions = int(round(path_length / motif_length))

    # repeat the motif
    motif_tiled = tile_x(motif=motif, spacing=1, repetitions=repetitions)
    motif_tiled[:, 0] /= repetitions

    # place it on the path
    stitches = motif_to_path(motif_tiled, path)
    return stitches
