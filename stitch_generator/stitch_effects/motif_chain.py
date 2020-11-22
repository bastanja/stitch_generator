import numpy as np

from stitch_generator.functions.place_motif import place_motif_between
from stitch_generator.path.path import Path
from stitch_generator.stitch_effects.stitch_effect import StitchEffect
from stitch_generator.utilities.types import SamplingFunction, Array2D


def motif_chain(motif_position_sampling: SamplingFunction, motif_generator, length: float) -> StitchEffect:
    return lambda path: _motif_chain(path, motif_position_sampling=motif_position_sampling,
                                     motif_generator=motif_generator, length=length)


def _motif_chain(path: Path, motif_position_sampling: SamplingFunction, motif_generator, length) -> Array2D:
    motif_boundaries = motif_position_sampling(length)
    motif_points = path.position(motif_boundaries)

    motifs = [place_motif_between(p1, p2, next(motif_generator)) for p1, p2 in zip(motif_points, motif_points[1:])]

    motifs.append([motif_points[-1]])

    return np.concatenate(motifs)
