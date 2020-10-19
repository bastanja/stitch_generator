import numpy as np

from stitch_generator.design_utilities.embroidery_design import EmbroideryDesign
from stitch_generator.design_utilities.palette import palette
from stitch_generator.design_utilities.parameter import FloatParameter, RampParameter, BoolParameter
from stitch_generator.functions.embroidery_pattern import EmbroideryPattern
from stitch_generator.functions.function_modifiers import multiply
from stitch_generator.functions.functions_1d import constant
from stitch_generator.functions.functions_2d import line, constant_direction, bezier_normals, bezier
from stitch_generator.functions.path import Path
from stitch_generator.stitch_effects.contour import contour_along
from stitch_generator.stitch_effects.variable_running_stitch import variable_underlay, variable_running_stitch


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="variable_running_stitch", parameters={
            'length': FloatParameter("Length", 10, 50, 120),
            'curve_ratio': FloatParameter("Curve Ratio", -1, 0.1, 1),
            'spacing': FloatParameter("Stroke spacing", 0.3, 1, 10),
            'stitch_length': FloatParameter("Stitch Length", 1, 3, 6),
            'width_scale': FloatParameter("Width Scale", 0, 10.5, 50),
            'width': RampParameter("Width", np.array(((0, 0), (0.5, 1), (1, 0)))),
            'alignment': FloatParameter("Stroke alignment", 0, 0.5, 1),
            'contour': BoolParameter("Show Contour", False)
        })

    def get_pattern(self, parameters):
        parameters = self.validate(parameters)

        color = palette()

        l = parameters.length
        w = parameters.length * parameters.curve_ratio

        control_points = ((0, 0), (l / 3, -w), (2 * l / 3, w), (l, 0))

        f = bezier(control_points)
        direction = bezier_normals(control_points)

        width = multiply(constant(parameters.width_scale), parameters.width)
        path = Path(position=f, direction=direction, width=width, stroke_alignment=constant(parameters.alignment))

        stitches = variable_running_stitch(path, parameters.spacing, stitch_length=parameters.stitch_length)
        stitches2 = variable_underlay(path, parameters.spacing, stitch_length=parameters.stitch_length)
        pattern = EmbroideryPattern()
        pattern.add_stitches(stitches, next(color))
        pattern.add_stitches(stitches2 + (0, 20), next(color))

        if parameters.contour:
            pattern.add_stitches(contour_along(path, stitch_length=1), next(color))
            pattern.add_stitches(contour_along(path, stitch_length=1) + (0, 20), next(color))

        return pattern


if __name__ == "__main__":
    Design().cli()
