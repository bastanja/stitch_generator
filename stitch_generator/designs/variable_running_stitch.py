from stitch_generator.design_utilities.embroidery_design import EmbroideryDesign
from stitch_generator.design_utilities.parameter import FloatParameter, IntParameter
from stitch_generator.functions.calculate_direction import calculate_direction
from stitch_generator.functions.embroidery_pattern import EmbroideryPattern
from stitch_generator.functions.function_modifiers import scale, add, inverse, repeat, shift, multiply
from stitch_generator.functions.functions_1d import constant, sinus
from stitch_generator.functions.functions_2d import line, function_2d, circle
from stitch_generator.functions.path import Path
from stitch_generator.stitch_effects.variable_running_stitch import variable_running_stitch


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="variable_running_stitch", parameters={
            'loops': IntParameter("Number of Loops", 1, 5, 10),
            'spacing': FloatParameter("Stroke spacing", 0.1, 0.2, 3),
            'width': FloatParameter("Width", 0, 75, 200),
            'stitch_length': FloatParameter("Stitch Length", 1, 3, 6),
            'loop_scale_x': FloatParameter("Loop Scale X", 0, 8, 30),
            'loop_scale_y': FloatParameter("Loop Scale Y", 0, 10, 60),
            'width_shift': FloatParameter("Width Shift", -0.5, 0, 0.5),
            'width_scale': FloatParameter("Width Scale", 0, 2, 8)
        })

    def get_pattern(self, parameters):
        parameters = self.validate(parameters)
        f = line((0, 0), (parameters.width, 0))

        direction = repeat(parameters.loops, shift(0.75, inverse(circle())))
        direction_scale = function_2d(constant(parameters.loop_scale_x), constant(parameters.loop_scale_y))
        direction = multiply(direction, direction_scale)
        width = repeat((parameters.loops), shift(parameters.width_shift + 0.5, add(scale(0.5, sinus()), constant(0.5))))
        width = multiply(constant(parameters.width_scale), width)

        f = add(f, direction)

        direction = lambda v: calculate_direction(f(v))

        path = Path(position=f, direction=direction, width=width, stroke_alignment=constant(0))

        stitches = variable_running_stitch(path, parameters.spacing, stitch_length=parameters.stitch_length)
        pattern = EmbroideryPattern()
        pattern.add_stitches(stitches)

        return pattern


if __name__ == "__main__":
    Design().cli()
