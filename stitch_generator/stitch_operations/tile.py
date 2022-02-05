import numpy as np

from stitch_generator.framework.types import Array2D


def tile_x(motif: Array2D, spacing: float, repetitions: int) -> Array2D:
    """
    Copies a motif 'repetitions' times and moves each copy by 'spacing' along the x-axis

    Returns:
        The tiled motif
    """
    return tile(motif, spacing, repetitions, 0)


def tile_y(motif: Array2D, spacing: float, repetitions: int) -> Array2D:
    """
    Copies a motif 'repetitions' times and moves each copy by 'spacing' along the y-axis

    Returns:
        The tiled motif
    """
    return tile(motif, spacing, repetitions, 1)


def tile(motif: Array2D, spacing: float, repetitions: int, axis: int) -> Array2D:
    # repeat the motif
    motif_tiled = np.tile(motif, reps=(repetitions, 1))

    # calculate offset for each motif repetition
    motif_offsets = np.arange(start=0, stop=repetitions) * spacing

    # repeat each offset for each point of the motif
    offsets = np.repeat(motif_offsets, repeats=len(motif))

    # add offsets to the motif points
    motif_tiled[:, axis] += offsets

    return motif_tiled
