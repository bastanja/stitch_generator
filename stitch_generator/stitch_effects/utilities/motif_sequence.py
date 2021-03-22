import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.functions.function_modifiers import rotate_degrees
from stitch_generator.functions.place_motif import place_motif_at
from stitch_generator.utilities.types import SamplingFunction, Array2D, Function1D


def motif_sequence_along(path: Path, motif_position_sampling: SamplingFunction, motif_generator,
                         motif_rotation_degrees: Function1D) -> Array2D:
    motif_locations = motif_position_sampling(path.length)

    rotation = rotate_degrees(path.direction, motif_rotation_degrees)
    motifs = [place_motif_at(path.position(t), rotation(t)[0], 1, next(motif_generator), include_endpoint=True) for t in
              motif_locations]

    return np.concatenate(motifs)
