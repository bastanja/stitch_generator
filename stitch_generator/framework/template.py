from stitch_generator.framework.embroidery_design import EmbroideryDesign
from stitch_generator.framework.parameter import FloatParameter
from stitch_generator.framework.path import Path
from stitch_generator.functions.functions_1d import constant
from stitch_generator.shapes.circle import circle
from stitch_generator.stitch_effects.contour import contour


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="template_design", parameters={
            'stitch_length': FloatParameter("Stitch length", 1, 3, 6),
            'radius': FloatParameter("Radius", 10, 20, 50),
            'width': FloatParameter("Line Width", 1, 10, 50),
        })

    def _to_pattern(self, parameters, pattern):
        path = Path(shape=circle(parameters.radius), direction=circle(),
                    width=constant(parameters.width), stroke_alignment=constant(0.5))
        stitch_effect = contour(stitch_length=parameters.stitch_length)
        stitches = stitch_effect(path)
        pattern.add_stitches(stitches)


if __name__ == "__main__":
    Design().cli()
