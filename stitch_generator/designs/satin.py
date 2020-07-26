import numpy as np

from stitch_generator.design_utilities.embroidery_design import EmbroideryDesign
from stitch_generator.design_utilities.palette import palette
from stitch_generator.design_utilities.parameter import FloatParameter
from stitch_generator.functions.connect_functions import alternate_direction, combine_start_end
from stitch_generator.functions.embroidery_pattern import EmbroideryPattern
from stitch_generator.functions.function_modifiers import combine, multiply, subtract
from stitch_generator.functions.function_sequence import function_sequence
from stitch_generator.functions.functions_1d import linear_interpolation, constant, arc
from stitch_generator.functions.functions_2d import line, constant_direction
from stitch_generator.stitch_effects.meander import meander_along
from stitch_generator.stitch_effects.satin import satin_along


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="satin", parameters={
            'stitch_spacing': FloatParameter("Stitch spacing", 0.1, 0.2, 1),
            'stitch_length': FloatParameter("Stitch length", 1, 2.5, 10),
            'length': FloatParameter("Length", 10, 30, 200),
            'min_width': FloatParameter("Min Width ", 0, 0, 12),
            'max_width': FloatParameter("Max Width", 0, 10, 40),
            'alignment': FloatParameter("Alignment", 0, 0.5, 1),
            'pattern_alignment': FloatParameter("Pattern Alignment", 0, 0.5, 1),
        })

    def get_pattern(self, parameters):
        parameters = self.validate(parameters)
        f = line((0, 0), (parameters.length, 0))
        direction = constant_direction(0, -1)

        width = self._get_width_function(parameters)

        stitches = [
            satin_along(f, direction, width, constant(parameters.alignment), parameters.stitch_spacing,
                        alternate_direction(parameters.stitch_length, parameters.pattern_alignment,
                                            include_endpoint=False), parameters.length),
            meander_along(f, direction, width, constant(parameters.alignment), parameters.stitch_spacing,
                          combine_start_end(alternate_direction(parameters.stitch_length, parameters.pattern_alignment,
                                                                include_endpoint=True)), parameters.length)
        ]

        pattern = EmbroideryPattern()
        col = palette()

        offset = 0
        for s in stitches:
            s += np.array((0, offset))
            pattern.add_stitches(s, next(col))
            offset += parameters.max_width + 5
        return pattern

    def _get_width_function(self, parameters):
        widths = [linear_interpolation(0, 1),
                  subtract(constant(1), multiply(constant(0.7), arc())),
                  linear_interpolation(1, 0)]
        segment_lengths = (parameters.max_width / 2, parameters.length - parameters.max_width, parameters.max_width / 2)
        width = function_sequence(widths, segment_lengths)
        width = combine(width, linear_interpolation(parameters.min_width, parameters.max_width))
        return width


if __name__ == "__main__":
    Design().cli()
