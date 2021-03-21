import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.functions.function_modifiers import rotate_degrees
from stitch_generator.functions.functions_1d import constant
from stitch_generator.functions.motif_generators import repeat_motif
from stitch_generator.functions.place_motif import place_motif_at
from stitch_generator.motifs.zigzag import zigzag
from stitch_generator.utilities.types import SamplingFunction


def stem_stitch(motif_position_sampling: SamplingFunction, stitch_width: float, stitch_length: float,
                repetitions: int, stitch_rotation: float):
    return lambda path: stem_stitch_along(path, motif_position_sampling, stitch_width, stitch_length, repetitions,
                                          stitch_rotation)


def stem_stitch_along(path: Path, motif_position_sampling: SamplingFunction, stitch_width: float, stitch_length: float,
                      repetitions: int, stitch_rotation: float):
    motif = zigzag(stitch_width, stitch_length, repetitions)

    rotation = rotate_degrees(path.direction, constant(stitch_rotation))
    motif_locations = motif_position_sampling(path.length)

    motif_generator = repeat_motif(motif)

    motifs = [place_motif_at(path.position(t), rotation(t)[0], 1, next(motif_generator)) for t in motif_locations]

    return np.concatenate(motifs)
