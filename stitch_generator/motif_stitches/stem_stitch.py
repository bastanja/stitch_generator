from stitch_generator.functions.functions_1d import constant
from stitch_generator.functions.motif_generators import repeat_motif
from stitch_generator.motifs.zigzag import zigzag
from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.stitch_effects.utilities.motif_sequence import motif_sequence_along


def stem_stitch(spacing: float, stitch_width: float, stitch_length: float,
                repetitions: int, stitch_rotation: float):
    motif = zigzag(stitch_width, stitch_length, repetitions)
    motif_generator = repeat_motif(motif)
    return lambda path: motif_sequence_along(path=path,
                                             motif_position_sampling=regular(spacing),
                                             motif_generator=motif_generator,
                                             motif_rotation_degrees=constant(stitch_rotation))
