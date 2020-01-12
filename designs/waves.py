import numpy as np
from designs.parameter import FloatParameter, IntParameter
from lib.embroidery_pattern import EmbroideryPattern
from lib.sample import sample
from designs.embroidery_design import EmbroideryDesign
from lib.function_modifiers import shift, scale, repeat, add, combine
from lib.functions_1d import cosinus, linear_interpolation, constant
from lib.functions_2d import function_2d


class Waves(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self)
        self.parameters = {'width': FloatParameter("Width", 100, 200, 500),
                           'points_per_row': IntParameter("Points per Row", 30, 70, 160),
                           'wave_length': FloatParameter("Wave Length", 10, 70, 100),
                           'wave_height': FloatParameter("Wave Height", 0, 4, 20),
                           'initial_offset': FloatParameter("Initial Offset", -0.5, 0, 0.5),
                           'offset_per_line': FloatParameter("Offset per Line", -0.5, 0.25, 0.5),
                           'line_distance': FloatParameter("Line Distance", 1, 8, 50),
                           'number_of_lines': IntParameter("Number of Lines", 2, 20, 50)}

        self.set_own_attributes()

    def get_pattern(self):
        repetitions = self.width / self.wave_length

        stitches = np.empty([0, 2])

        for i in range(0, self.number_of_lines):
            initial_offset = self.initial_offset + i * self.offset_per_line
            f_x = linear_interpolation(0, self.width)
            f_y = shift(initial_offset, cosinus())
            f_y = scale(self.wave_height, repeat(repetitions, f_y))
            f_y = add(constant(i * self.line_distance), f_y)
            f = function_2d(f_x, f_y)

            if i % 2 == 1:
                inverse = linear_interpolation(1, 0)
                f = combine(f, inverse)

            additional_stitches = sample(f, self.points_per_row)
            stitches = np.concatenate((stitches, additional_stitches))

        pattern = EmbroideryPattern()
        pattern.add_stitches(stitches)

        return pattern
