from stitch_generator.design_utilities.embroidery_design import EmbroideryDesign
from stitch_generator.design_utilities.palette import palette
from stitch_generator.design_utilities.parameter import FloatParameter
from stitch_generator.functions.embroidery_pattern import EmbroideryPattern
from stitch_generator.functions.functions_1d import constant
from stitch_generator.functions.functions_2d import line, constant_direction
from stitch_generator.functions.path import Path
from stitch_generator.stitch_effects.contour import contour


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="template_design", parameters={
            'stitch_length': FloatParameter("Stitch length", 1, 3, 6),
            'length': FloatParameter("Length", 10, 80, 200),
        })

    def get_pattern(self, parameters):
        parameters = self.validate(parameters)
        color = palette()

        path = Path(position=line((0, 0), (parameters.length, 0)), direction=constant_direction(0, -1),
                    width=constant(1), stroke_alignment=constant(0.5))

        stitches = contour(path=path, stitch_length=parameters.stitch_length)

        pattern = EmbroideryPattern()
        pattern.add_stitches(stitches, next(color))

        return pattern


if __name__ == "__main__":
    Design().cli()
