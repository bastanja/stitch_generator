import numpy as np

from stitch_generator.framework.embroidery_design import EmbroideryDesign
from stitch_generator.framework.parameter import FloatParameter, BoolParameter
from stitch_generator.framework.path import Path
from stitch_generator.functions.function_modifiers import mix, scale
from stitch_generator.functions.functions_1d import constant, arc
from stitch_generator.functions.functions_2d import constant_direction
from stitch_generator.shapes.circle import circle
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.collection import stitch_effects


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="stitch_effects", parameters={
            'stitch_length': FloatParameter("Stitch length", 1, 3, 6),
            'length': FloatParameter("Length", 10, 100, 200),
            'width_factor': FloatParameter("Width Factor", 0, 0, 1),
            'circular': BoolParameter("Circular", False)
        })

    def _to_pattern(self, parameters, pattern, color):
        width_f = mix(constant(10), scale(10, arc), constant(parameters.width_factor))

        if parameters.circular:
            path = Path(shape=scale(parameters.length / 4, circle()),
                        direction=circle(),
                        width=width_f,
                        stroke_alignment=constant(0.5))
            offset = (0, (parameters.length / 2) + 20)
        else:
            path = Path(shape=line((0, 0), (parameters.length, 0)),
                        direction=constant_direction(0, -1),
                        width=width_f,
                        stroke_alignment=constant(0.5))
            offset = (0, 15)

        effects = list(iter(stitch_effects(parameters.stitch_length)))
        offsets = [np.array(offset) * i for i in range(len(effects))]

        for effect, offset in zip(effects, offsets):
            pattern.add_stitches(effect(path) + offset, next(color))


if __name__ == "__main__":
    Design().cli()
