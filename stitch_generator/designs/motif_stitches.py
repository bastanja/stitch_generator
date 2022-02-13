import numpy as np

from stitch_generator.framework.embroidery_design import EmbroideryDesign
from stitch_generator.framework.palette import palette
from stitch_generator.framework.parameter import FloatParameter
from stitch_generator.framework.path import Path
from stitch_generator.functions.functions_1d import constant
from stitch_generator.functions.motif_generators import repeat_motif, alternate_direction
from stitch_generator.motifs.line import straight_line
from stitch_generator.motifs.zigzag import zigzag
from stitch_generator.sampling.sample_by_length import regular, sampling_by_length, sampling_by_length_with_offset
from stitch_generator.sampling.sampling_modifiers import free_start_end, remove_end
from stitch_generator.shapes.bezier import bezier, bezier_normals
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


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="motif_stitches", parameters={
            'stitch_length': FloatParameter("Stitch Length", 2, 3, 6),
            'length': FloatParameter("Length", 10, 110, 200),
            'spacing': FloatParameter("Spacing", 2, 2.5, 4),
            'pattern_spacing': FloatParameter("Pattern Spacing", 10, 20, 30)
        })

    def _to_pattern(self, parameters, pattern):
        color = palette()
        y_step = parameters.length / 3
        x = parameters.length / 4
        control_points = ((0, 0), (y_step, -x), (y_step * 2, x), (y_step * 3, 0))

        path = Path(shape=bezier(control_points), direction=bezier_normals(control_points))

        effects = [
            stem_stitch(spacing=parameters.spacing, stitch_width=0.6, stitch_length=4, repetitions=5, angle=25),
            stem_stitch(spacing=parameters.spacing, stitch_width=5, stitch_length=4, repetitions=5, angle=0),
            e_stitch(spacing=parameters.spacing, line_length=4, stitch_length=parameters.stitch_length, angle=45),
            three_arrows(start_end_spacing=parameters.pattern_spacing / 2, pattern_spacing=parameters.pattern_spacing,
                         stitch_length=parameters.stitch_length),
            arrow_chain(spacing=parameters.spacing)
        ]

        for i, stitch_effect in enumerate(effects):
            pattern.add_stitches(stitch_effect(path) + (0, i * 10), next(color))


if __name__ == "__main__":
    Design().cli()
