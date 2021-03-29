from stitch_generator.framework.embroidery_design import EmbroideryDesign
from stitch_generator.framework.embroidery_pattern import EmbroideryPattern
from stitch_generator.framework.palette import palette
from stitch_generator.framework.parameter import FloatParameter, IntParameter
from stitch_generator.framework.path import Path
from stitch_generator.functions.functions_1d import constant
from stitch_generator.functions.motif_generators import repeat_motif_mirrored
from stitch_generator.motif_stitches.e_stitch import e_stitch, alternating_e_stitch
from stitch_generator.motif_stitches.stem_stitch import stem_stitch
from stitch_generator.motif_stitches.twig import twig
from stitch_generator.motifs.heart import heart
from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.shapes.bezier import bezier, bezier_normals
from stitch_generator.stitch_effects.motif_chain import motif_chain


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="motif_stitches", parameters={
            'stitch_spacing': FloatParameter("Stitch spacing", 1, 3, 20),
            'length': FloatParameter("Length", 10, 80, 200),
            'stitch_width': FloatParameter("Stitch Width", 0.1, 0.8, 10),
            'stem_stitch_length': FloatParameter("Stem stitch Length", 1, 4, 15),
            'angle': FloatParameter("Angle", -180, 20, 180),
            'repetitions': IntParameter("Repetitions", 2, 5, 12),
            'leaf_spacing': FloatParameter("Leaf spacing", 3, 7, 15),
            'leaf_angle_left': FloatParameter("Leaf Angle", 0, 45, 90),
            'leaf_angle_right': FloatParameter("Leaf Angle", -90, -45, 0),
            'stitch_length': FloatParameter("Stitch Length", 1, 2.5, 5),
            'heart_spacing': FloatParameter("Heart spacing", 4, 8, 15)
        })

    def get_pattern(self, parameters):
        parameters = self.validate(parameters)
        color = palette()

        l = -parameters.length / 3
        w = parameters.length / 4
        control_points = ((0, 0), (-w, l), (w, l * 2), (0, l * 3))

        f = bezier(control_points)
        direction = bezier_normals(control_points)

        path = Path(position=f, direction=direction, width=constant(1), stroke_alignment=constant(0.5))

        effects = [
            stem_stitch(
                spacing=parameters.stitch_spacing,
                stitch_width=parameters.stitch_width, stitch_length=parameters.stem_stitch_length,
                repetitions=parameters.repetitions, stitch_rotation=parameters.angle),
            stem_stitch(
                spacing=2.5,
                stitch_width=5, stitch_length=parameters.stem_stitch_length,
                repetitions=parameters.repetitions, stitch_rotation=0),
            e_stitch(
                spacing=parameters.stitch_spacing, line_length=parameters.stem_stitch_length,
                stitch_length=parameters.stem_stitch_length, stitch_rotation=parameters.angle),
            alternating_e_stitch(
                spacing=parameters.stitch_spacing, line_length=parameters.stem_stitch_length,
                stitch_length=parameters.stem_stitch_length, stitch_rotation=0),
            twig(stem_length=2, leaf_length=7, leaf_width=3, spacing=parameters.leaf_spacing,
                 start_length=parameters.leaf_spacing, end_length=parameters.leaf_spacing,
                 stitch_length=parameters.stitch_length, angle_left=parameters.leaf_angle_left,
                 angle_right=parameters.leaf_angle_right),
            motif_chain(regular(parameters.heart_spacing), repeat_motif_mirrored(heart(parameters.heart_spacing)))
        ]

        pattern = EmbroideryPattern()

        for i, stitch_effect in enumerate(effects):
            pattern.add_stitches(stitch_effect(path) + (20 * i, 0), next(color))

        return pattern


if __name__ == "__main__":
    Design().cli()
