from stitch_generator.framework.embroidery_design import EmbroideryDesign
from stitch_generator.framework.embroidery_pattern import EmbroideryPattern
from stitch_generator.framework.palette import palette
from stitch_generator.framework.parameter import FloatParameter, IntParameter
from stitch_generator.framework.path import Path
from stitch_generator.functions.functions_1d import constant
from stitch_generator.motif_stitches.e_stitch import e_stitch, alternating_e_stitch
from stitch_generator.motif_stitches.stem_stitch import stem_stitch
from stitch_generator.shapes.bezier import bezier, bezier_normals


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="motif_stitches", parameters={
            'stitch_spacing': FloatParameter("Stitch spacing", 1, 3, 20),
            'length': FloatParameter("Length", 10, 80, 200),
            'stitch_width': FloatParameter("Stitch Width", 0.1, 0.8, 10),
            'stitch_length': FloatParameter("Stitch Length", 1, 4, 15),
            'angle': FloatParameter("Angle", -180, 20, 180),
            'repetitions': IntParameter("Repetitions", 2, 5, 12),
        })

    def get_pattern(self, parameters):
        parameters = self.validate(parameters)
        color = palette()

        l = parameters.length
        w = parameters.length / 3
        control_points = ((0, 0), (l / 3, -w), (2 * l / 3, w), (l, 0))

        f = bezier(control_points)
        direction = bezier_normals(control_points)

        path = Path(position=f, direction=direction, width=constant(1), stroke_alignment=constant(0.5))
        pattern = EmbroideryPattern()

        stitch_effect = stem_stitch(
            spacing=parameters.stitch_spacing,
            stitch_width=parameters.stitch_width, stitch_length=parameters.stitch_length,
            repetitions=parameters.repetitions, stitch_rotation=parameters.angle)
        pattern.add_stitches(stitch_effect(path), next(color))

        stitch_effect = e_stitch(
            spacing=parameters.stitch_spacing, line_length=parameters.stitch_length,
            stitch_length=parameters.stitch_length, stitch_rotation=parameters.angle)
        pattern.add_stitches(stitch_effect(path) + (0, 20), next(color))

        stitch_effect = alternating_e_stitch(
            spacing=parameters.stitch_spacing, line_length=parameters.stitch_length,
            stitch_length=parameters.stitch_length, stitch_rotation=0)
        pattern.add_stitches(stitch_effect(path) + (0, 40), next(color))



        return pattern


if __name__ == "__main__":
    Design().cli()
