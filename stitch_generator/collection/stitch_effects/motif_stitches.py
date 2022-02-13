import numpy as np

from stitch_generator.collection.motifs.collection import zigzag, zigzag_motif, rhomb_motif, x_motif, line_motif, \
    overlock_stitch_motif
from stitch_generator.collection.motifs.line import straight_line
from stitch_generator.framework.path import Path, get_boundaries
from stitch_generator.functions.function_modifiers import mix, inverse
from stitch_generator.functions.functions_1d import constant
from stitch_generator.functions.motif_generators import repeat_motif, alternate_direction
from stitch_generator.sampling.sample_by_length import sampling_by_length, sampling_by_length_with_offset, regular
from stitch_generator.sampling.sampling_modifiers import remove_end, free_start_end, add_end, add_start
from stitch_generator.stitch_effects.path_effects.tile_motif import tile_motif
from stitch_generator.stitch_effects.shape_effects.motif_chain import motif_chain
from stitch_generator.stitch_effects.shape_effects.motif_to_points import motif_to_points
from stitch_generator.stitch_effects.shape_effects.motif_to_segments import motif_to_segments
from stitch_generator.stitch_operations.rotate import rotate_by_degrees


def e_stitch(spacing: float, line_length: float, stitch_length: float, angle: float):
    motif = rotate_by_degrees(straight_line(line_length, line_length), angle)
    motif_generator = repeat_motif(motif)
    sampling = remove_end(sampling_by_length(stitch_length))

    return motif_to_points(motif_position_sampling=sampling_by_length(spacing),
                           line_sampling=sampling,
                           motif_generator=motif_generator)


def stem_stitch(spacing: float, stitch_width: float, stitch_length: float, repetitions: int, angle: float):
    motif = zigzag(stitch_width, stitch_length, repetitions)
    motif_generator = repeat_motif(motif)
    sampling = sampling_by_length_with_offset(segment_length=spacing, offset=0.5)

    return motif_chain(motif_position_sampling=sampling,
                       motif_generator=motif_generator,
                       motif_rotation_degrees=constant(angle))


def three_arrows(start_end_spacing: float, pattern_spacing: float, stitch_length: float):
    single_arrow = np.array(((0, 0.0), (-3, -3), (0, 0), (-3, 3), (0, 0)))
    arrow_spacing = 2
    combined = np.concatenate((single_arrow, single_arrow + (arrow_spacing, 0), single_arrow + (arrow_spacing * 2, 0)))
    motif_sampling = free_start_end(start_end_spacing, start_end_spacing, regular(pattern_spacing))
    return motif_to_segments(motif_sampling, regular(stitch_length), repeat_motif(combined), motif_length=3)


def arrow_chain(spacing: float):
    single_arrow = np.array(((-2, -2), (0, 0), (2, -2)))
    motif_gen = alternate_direction(repeat_motif(single_arrow))
    sampling = sampling_by_length(spacing)
    return motif_chain(sampling, motif_gen, constant(0))


def cretan_stitch(spacing: float, width: float, height: float, repetitions: int, zig_zag_height: float = 0):
    motif = zigzag_motif(width, height, repetitions) + (zig_zag_height, 0)
    motif_gen = alternate_direction(repeat_motif(motif))
    sampling = sampling_by_length(spacing)
    return motif_chain(sampling, motif_gen, constant(0))


def feather_stitch(spacing: float, width: float, height: float, repetitions: int):
    motif = rotate_by_degrees(zigzag_motif(width, height, repetitions), 45) + (1, 0)
    motif_gen = alternate_direction(repeat_motif(motif))
    sampling = sampling_by_length(spacing)
    return motif_chain(sampling, motif_gen, constant(0))


def rhomb_motif_stitch(spacing: float, width: float, height: float):
    motif = rotate_by_degrees(rhomb_motif(width, height), -90)
    motif_gen = repeat_motif(motif)
    sampling = sampling_by_length(spacing)
    return motif_chain(sampling, motif_gen, constant(0))


def x_motif_stitch(spacing: float, width: float, height: float):
    motif = x_motif(width, height)
    motif_gen = repeat_motif(motif)
    sampling = sampling_by_length(spacing)
    return motif_chain(sampling, motif_gen, constant(0))


def alternating_triangles(spacing: float, line_length: float, zig_zag_height: float, repetitions: int):
    motif = zigzag(width=0.1, height=-line_length, repetitions=repetitions) + (zig_zag_height, 0)
    motif_gen = alternate_direction(repeat_motif(motif))
    sampling = sampling_by_length(spacing)
    return motif_chain(sampling, motif_gen, constant(0))


def chevron_stitch(spacing: float, line_length: float, zig_zag_height: float, repetitions: int):
    motif = line_motif(line_length, repetitions) + (zig_zag_height, 0)
    motif_gen = alternate_direction(repeat_motif(motif))
    sampling = sampling_by_length(spacing)
    return motif_chain(sampling, motif_gen, constant(0))


def overlock_stitch(spacing: float, width: float):
    loop_ratio = 0.4
    motif = overlock_stitch_motif(1, 1, loop_ratio)
    stitch_effect = tile_motif(motif=motif, motif_length=spacing)
    back_stitch_sampling = add_start(add_end(sampling_by_length_with_offset(segment_length=spacing, offset=0.5)))

    def effect(path):
        constant_width_path = Path(path.shape, path.direction, constant(width), constant(0.5))
        left, right = get_boundaries(constant_width_path)
        samples = back_stitch_sampling(constant_width_path.length)
        back_stitch_line = inverse(mix(right, left, constant(loop_ratio)))

        stitches = stitch_effect(constant_width_path)
        back_stitches = back_stitch_line(samples)

        return np.concatenate((stitches, right(1), left(1), back_stitches))

    return effect
