from stitch_generator.functions.motif_generators import repeat_motif, repeat_motif_mirrored
from stitch_generator.motifs.line import straight_line
from stitch_generator.sampling.sample_by_length import sampling_by_length
from stitch_generator.sampling.sampling_modifiers import remove_end
from stitch_generator.stitch_effects.utilities.motif_to_points import motif_to_points_along
from stitch_generator.stitch_operations.rotate import rotate_by_degrees


def e_stitch(spacing: float, line_length: float, stitch_length: float, stitch_rotation: float):
    motif = rotate_by_degrees(straight_line(line_length, stitch_length), stitch_rotation)
    motif_generator = repeat_motif(motif)

    return lambda path: motif_to_points_along(path,
                                              motif_position_sampling=sampling_by_length(spacing),
                                              line_sampling=remove_end(sampling_by_length(stitch_length)),
                                              motif_generator=motif_generator)


def alternating_e_stitch(spacing: float, line_length: float, stitch_length: float, stitch_rotation: float):
    motif = rotate_by_degrees(straight_line(line_length, stitch_length), stitch_rotation)
    motif_generator = repeat_motif_mirrored(motif)

    return lambda path: motif_to_points_along(path,
                                              motif_position_sampling=sampling_by_length(spacing),
                                              line_sampling=remove_end(sampling_by_length(stitch_length)),
                                              motif_generator=motif_generator)
