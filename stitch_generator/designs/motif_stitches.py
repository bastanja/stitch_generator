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
from stitch_generator.stitch_effects.motif_sequence import motif_sequence
from stitch_generator.stitch_effects.shape_effects.segment_motif_to_shape import segment_motif
from stitch_generator.stitch_effects.utilities.motif_sequence import motif_sequence_along
from stitch_generator.stitch_effects.utilities.motif_to_points import motif_to_points_along
from stitch_generator.stitch_operations.rotate import rotate_by_degrees


def e_stitch(spacing: float, line_length: float, stitch_length: float, stitch_rotation: float):
    motif = rotate_by_degrees(straight_line(line_length, stitch_length), stitch_rotation)
    motif_generator = repeat_motif(motif)

    return lambda path: motif_to_points_along(path,
                                              motif_position_sampling=sampling_by_length(spacing),
                                              line_sampling=remove_end(sampling_by_length(stitch_length)),
                                              motif_generator=motif_generator)


def stem_stitch(spacing: float, stitch_width: float, stitch_length: float,
                repetitions: int, stitch_rotation: float):
    motif = zigzag(stitch_width, stitch_length, repetitions)
    motif_generator = repeat_motif(motif)
    sampling = sampling_by_length_with_offset(segment_length=spacing, offset=0.5)
    return lambda path: motif_sequence_along(path=path,
                                             motif_position_sampling=sampling,
                                             motif_generator=motif_generator,
                                             motif_rotation_degrees=constant(stitch_rotation))


def three_arrows():
    single_arrow = np.array(((0, 0.0), (-3, -3), (0, 0), (-3, 3), (0, 0)))
    combined = np.concatenate((single_arrow, single_arrow + (2, 0), single_arrow + (4, 0)))
    return segment_motif(
        free_start_end(10, 10, regular(20)), regular(3), repeat_motif(combined), motif_length=3)


def arrow_chain():
    single_arrow = np.array(((-2, -2), (0, 0), (2, -2)))
    motif_gen = alternate_direction(repeat_motif(single_arrow))
    sampling = sampling_by_length(2)

    return motif_sequence(sampling, motif_gen, constant(0))


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="motif_stitches", parameters={
            'length': FloatParameter("Length", 10, 110, 200)
        })

    def _to_pattern(self, parameters, pattern):
        color = palette()
        y_step = parameters.length / 3
        x = parameters.length / 4
        control_points = ((0, 0), (y_step, -x), (y_step * 2, x), (y_step * 3, 0))

        path = Path(shape=bezier(control_points), direction=bezier_normals(control_points))

        stem_stitch_width = 0.6
        stem_stitch_length = 4

        effects = [
            stem_stitch(
                spacing=2, stitch_width=stem_stitch_width, stitch_length=stem_stitch_length, repetitions=5,
                stitch_rotation=25),
            stem_stitch(
                spacing=2.5, stitch_width=5, stitch_length=stem_stitch_length, repetitions=5, stitch_rotation=0),
            e_stitch(
                spacing=2, line_length=stem_stitch_length, stitch_length=stem_stitch_length, stitch_rotation=45),
            three_arrows(),
            arrow_chain()
        ]

        for i, stitch_effect in enumerate(effects):
            pattern.add_stitches(stitch_effect(path) + (0, i * 10), next(color))


if __name__ == "__main__":
    Design().cli()
