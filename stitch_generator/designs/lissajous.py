from stitch_generator.framework.embroidery_design import EmbroideryDesign
from stitch_generator.framework.palette import palette
from stitch_generator.framework.parameter import FloatParameter, IntParameter, BoolParameter
from stitch_generator.functions.arc_length_mapping import arc_length_mapping_with_length
from stitch_generator.framework.embroidery_pattern import EmbroideryPattern
from stitch_generator.functions.function_modifiers import repeat, scale, shift, combine
from stitch_generator.functions.functions_1d import sinus
from stitch_generator.functions.functions_2d import function_2d
from stitch_generator.sampling.sample_by_length import sample_by_length


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="lissajous", parameters={
            'stitch_length': FloatParameter("Stitch Length", 0.5, 3, 6),
            'width': FloatParameter("Width", 30, 40, 200),
            'height': FloatParameter("Height", 30, 40, 200),
            'shift_x': FloatParameter("Shift X", -0.5, 0, 0.5),
            'shift_y': FloatParameter("Shift Y", -0.5, 0, 0.5),
            'repetitions_x': IntParameter("Repetitions X", 1, 3, 25),
            'repetitions_y': IntParameter("Repetitions Y", 1, 4, 25),
            'arc_length': BoolParameter("Arc Length Param", True)
        })

    def get_pattern(self, parameters):
        parameters = self.validate(parameters)
        color = palette()

        x = repeat(parameters.repetitions_x, scale(parameters.width/2, shift(parameters.shift_x, sinus())))
        y = repeat(parameters.repetitions_y, scale(parameters.height/2, shift(parameters.shift_y, sinus())))

        f = function_2d(x, y)

        mapping, length = arc_length_mapping_with_length(f, approximation_samples=10000)
        if parameters.arc_length:
            f = combine(mapping, f)

        samples = sample_by_length(total_length=length, segment_length=parameters.stitch_length, include_endpoint=True)

        pattern = EmbroideryPattern()
        pattern.add_stitches(f(samples), next(color))

        return pattern


if __name__ == "__main__":
    Design().cli()
