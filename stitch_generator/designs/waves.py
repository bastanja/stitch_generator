import numpy as np

from stitch_generator.design_utilities.embroidery_design import EmbroideryDesign
from stitch_generator.design_utilities.parameter import FloatParameter, IntParameter
from stitch_generator.functions.embroidery_pattern import EmbroideryPattern
from stitch_generator.functions.function_modifiers import shift, scale, repeat, add, inverse
from stitch_generator.functions.functions_1d import cosinus, linear_interpolation, constant
from stitch_generator.functions.functions_2d import function_2d
from stitch_generator.functions.samples import samples_by_segments
from stitch_generator.stitch_effects.running_stitch import running_stitch_line


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="waves", parameters={
            'width': FloatParameter("Width", 50, 120, 240),
            'stitch_length': FloatParameter("Stitch Length", 1, 3, 6),
            'wave_length': FloatParameter("Wave Length", 10, 70, 100),
            'wave_height': FloatParameter("Wave Height", 0, 4, 20),
            'initial_offset': FloatParameter("Initial Offset", -0.5, 0, 0.5),
            'offset_per_line': FloatParameter("Offset per Line", -0.5, 0.25, 0.5),
            'line_distance': FloatParameter("Line Distance", 1, 8, 50),
            'number_of_lines': IntParameter("Number of Lines", 2, 20, 50)
        })

    def get_pattern(self, parameters):
        parameters = self.validate(parameters)

        repetitions = parameters.width / parameters.wave_length

        stitches = []

        last_point = None

        for i in range(0, parameters.number_of_lines):
            initial_offset = parameters.initial_offset + i * parameters.offset_per_line
            fx = linear_interpolation(0, parameters.width)
            fy = shift(initial_offset, cosinus())
            fy = scale(parameters.wave_height, repeat(repetitions, fy))
            fy = add(constant(i * parameters.line_distance), fy)
            f = function_2d(fx, fy)

            if i % 2 == 1:
                f = inverse(f)

            if last_point is not None:
                fill_stitches = running_stitch_line(last_point, f(0)[0], parameters.stitch_length, False)
                if len(fill_stitches):
                    stitches.append(fill_stitches)

            p = samples_by_segments(int(parameters.width / parameters.stitch_length))
            current_line = f(p)
            stitches.append(current_line)

            last_point = f(1)[0]

        stitches.append([last_point])
        stitches = np.concatenate(stitches)
        pattern = EmbroideryPattern()
        pattern.add_stitches(stitches)

        return pattern


if __name__ == "__main__":
    Design().cli()
