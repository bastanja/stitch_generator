import numpy as np

from stitch_generator.framework.embroidery_design import EmbroideryDesign
from stitch_generator.framework.palette import palette
from stitch_generator.framework.parameter import FloatParameter
from stitch_generator.framework.path import Path
from stitch_generator.functions.functions_1d import constant
from stitch_generator.functions.motif_generators import repeat_motif, alternate_direction
from stitch_generator.motif_stitches.e_stitch import e_stitch, alternating_e_stitch
from stitch_generator.motif_stitches.stem_stitch import stem_stitch
from stitch_generator.sampling.sample_by_length import regular, sampling_by_length
from stitch_generator.sampling.sampling_modifiers import free_start_end
from stitch_generator.shapes.bezier import bezier, bezier_normals
from stitch_generator.stitch_effects.motif_sequence import motif_sequence
from stitch_generator.stitch_effects.motif_to_segments import motif_to_segments


def arrows():
    single_arrow = np.array(((0, 0.0), (-3, -3), (0, 0), (-3, 3), (0, 0)))
    combined = np.concatenate((single_arrow, single_arrow + (2, 0), single_arrow + (4, 0)))
    return motif_to_segments(
        free_start_end(10, 10, regular(20)), regular(3), repeat_motif(combined))


def arrows2():
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
            arrows(),
            arrows2()
        ]

        for i, stitch_effect in enumerate(effects):
            pattern.add_stitches(stitch_effect(path) + (0, i * 10), next(color))


if __name__ == "__main__":
    Design().cli()
