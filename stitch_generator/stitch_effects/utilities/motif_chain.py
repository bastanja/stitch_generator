import numpy as np

from stitch_generator.functions.place_motif import place_motif_between
from stitch_generator.path.path import Path
from stitch_generator.utilities.types import SamplingFunction, Array2D


def motif_chain_along(path: Path, motif_position_sampling: SamplingFunction, motif_generator) -> Array2D:
    motif_boundaries = motif_position_sampling(path.length)
    motif_points = path.position(motif_boundaries)

    motifs = [place_motif_between(p1, p2, next(motif_generator)) for p1, p2 in zip(motif_points, motif_points[1:])]

    motifs.append([motif_points[-1]])

    return np.concatenate(motifs)
