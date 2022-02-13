import itertools

import numpy as np

from stitch_generator.collection.motifs.line import straight_line
from stitch_generator.collection.motifs.zigzag import zigzag, zigzag_motif
from stitch_generator.framework.embroidery_design import EmbroideryDesign
from stitch_generator.framework.palette import palette
from stitch_generator.framework.parameter import FloatParameter
from stitch_generator.framework.path import Path
from stitch_generator.functions.arc_length_mapping import arc_length_mapping
from stitch_generator.functions.ensure_shape import ensure_2d_shape
from stitch_generator.functions.function_modifiers import combine, inverse
from stitch_generator.functions.functions_1d import constant
from stitch_generator.functions.motif_generators import repeat_motif, alternate_direction
from stitch_generator.sampling.sample_by_length import regular, sampling_by_length, sampling_by_length_with_offset
from stitch_generator.sampling.sampling_modifiers import free_start_end, remove_end, add_start, add_end
from stitch_generator.shapes.bezier import bezier, bezier_normals
from stitch_generator.stitch_effects.shape_effects.motif_chain import motif_chain
from stitch_generator.stitch_effects.shape_effects.motif_to_points import motif_to_points
from stitch_generator.stitch_effects.shape_effects.motif_to_segments import motif_to_segments
from stitch_generator.stitch_operations.rotate import rotate_by_degrees


# motifs

def rhomb_motif(width, height):
    half_width = width / 2
    half_height = height / 2
    return np.array(((-half_height, 0), (0, -half_width), (half_height, 0), (0, half_width), (-half_height, 0)))


def x_motif(width, height):
    half_width = width / 2
    half_height = height / 2
    motif = np.array(((0, 0), (-half_height, -half_width)))
    return np.concatenate((motif, motif * (1, -1), motif * (-1, -1), motif * (-1, 1), ensure_2d_shape((0, 0))))


def line_motif(length: float, repetitions: int):
    motif = zigzag(width=0.1, height=length, repetitions=repetitions)
    origin = ensure_2d_shape((0, 0))
    return np.concatenate((origin, motif, origin))


def loop_motif(width, height):
    stem_height = height / 3
    loop_height = height - stem_height

    return [(-stem_height, 0), (loop_height, 0), (loop_height, width), (0, width / 10), (-stem_height, 0)]


# motif stitches

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


def feather_stitch(spacing: float):
    motif = rotate_by_degrees(zigzag_motif(width=0.0, height=2.5, repetitions=2), 45) + (1, 0)
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


def loops(spacing: float, width: float, height: float):
    motif = np.array(loop_motif(width, height))
    motif_gen = repeat_motif(motif)
    sampling = sampling_by_length(spacing)

    loops_pattern = motif_chain(sampling, motif_gen, constant(0))
    sampling = add_start(add_end(sampling_by_length_with_offset(segment_length=spacing, offset=0.6)))

    def effect(path):
        stitches = loops_pattern(path)
        inverse_shape = inverse(path.shape)
        running_stitch_return = inverse_shape(sampling(path.length))
        return np.concatenate((stitches, running_stitch_return))

    return effect


# helper functions

def bezier_path(control_points):
    shape = bezier(control_points)
    param = arc_length_mapping(shape)
    shape = combine(param, shape)
    direction = combine(param, bezier_normals(control_points))
    return Path(shape=shape, direction=direction)


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="motif_stitches", parameters={
            'stitch_length': FloatParameter("Stitch Length", 2, 3, 6),
            'length': FloatParameter("Length", 10, 95, 200),
            'width': FloatParameter("Width", 0, 15, 50),
            'row_spacing': FloatParameter("Row Spacing", 5, 8, 12),
            'spacing': FloatParameter("Spacing", 2, 2.5, 4),
            'pattern_spacing': FloatParameter("Pattern Spacing", 10, 20, 30)
        })

    def _to_pattern(self, parameters, pattern):
        color = palette()

        effects = [
            stem_stitch(spacing=parameters.spacing, stitch_width=0.6, stitch_length=4, repetitions=5, angle=-25),
            stem_stitch(spacing=parameters.spacing, stitch_width=5, stitch_length=4, repetitions=5, angle=0),
            e_stitch(spacing=parameters.spacing, line_length=4, stitch_length=parameters.stitch_length, angle=45),
            three_arrows(start_end_spacing=parameters.pattern_spacing / 2, pattern_spacing=parameters.pattern_spacing,
                         stitch_length=parameters.stitch_length),
            arrow_chain(spacing=parameters.spacing),
            cretan_stitch(spacing=parameters.spacing, width=0.1, height=2.5, repetitions=4, zig_zag_height=1),
            cretan_stitch(spacing=parameters.spacing, width=0.1, height=3, repetitions=4),
            feather_stitch(spacing=parameters.spacing),
            rhomb_motif_stitch(spacing=parameters.spacing, width=3, height=5),
            x_motif_stitch(spacing=parameters.spacing, width=4, height=3),
            alternating_triangles(spacing=parameters.spacing, line_length=4, zig_zag_height=2, repetitions=3),
            chevron_stitch(spacing=parameters.spacing, line_length=3, zig_zag_height=2, repetitions=5),
            loops(spacing=parameters.spacing, width=parameters.spacing, height=5)
        ]

        y_step = parameters.length / 3
        x = parameters.width
        points = np.array(((0, 0), (y_step, -x), (y_step * 2, x), (y_step * 3, 0)))
        direction = itertools.cycle((False, True))
        offsets = [(0, i * parameters.row_spacing) for i in range(len(effects))]
        paths = [bezier_path(points + o) for o in offsets]
        paths = [p if dir else p.inverse() for p, dir in zip(paths, direction)]

        for i, stitch_effect in enumerate(effects):
            pattern.add_stitches(stitch_effect(paths[i]), next(color))


if __name__ == "__main__":
    Design().cli()
