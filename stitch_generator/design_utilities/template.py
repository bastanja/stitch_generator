from stitch_generator.design_utilities.embroidery_design import EmbroideryDesign
from stitch_generator.design_utilities.palette import palette
from stitch_generator.design_utilities.parameter import FloatParameter
from stitch_generator.functions.embroidery_pattern import EmbroideryPattern
from stitch_generator.functions.functions_2d import line
from stitch_generator.functions.samples import samples_by_length


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="template_design", parameters={
            'stitch_length': FloatParameter("Stitch length", 1, 3, 6),
            'length': FloatParameter("Length", 10, 80, 200),
        })

    def get_pattern(self, parameters):
        parameters = self.validate(parameters)
        color = palette()

        f = line((0, 0), (parameters.length, 0))
        t = samples_by_length(parameters.length, segment_length=parameters.stitch_length, include_endpoint=True)
        stitches = f(t)

        pattern = EmbroideryPattern()
        pattern.add_stitches(stitches, next(color))

        return pattern


if __name__ == "__main__":
    Design().cli()
