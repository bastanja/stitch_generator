import numpy as np

from stitch_generator.design_utilities.embroidery_design import EmbroideryDesign
from stitch_generator.design_utilities.palette import palette
from stitch_generator.design_utilities.parameter import FloatParameter
from stitch_generator.functions.embroidery_pattern import EmbroideryPattern
from stitch_generator.functions.function_modifiers import mix, scale
from stitch_generator.functions.functions_1d import constant, arc
from stitch_generator.functions.functions_2d import line, constant_direction
from stitch_generator.path.path import Path
from stitch_generator.stitch_effects.collection import stitch_effects


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="stitch_effects", parameters={
            'stitch_length': FloatParameter("Stitch length", 1, 3, 6),
            'length': FloatParameter("Length", 10, 80, 200),
            'width_factor': FloatParameter("Width Factor", 0, 0, 1)
        })

    def get_pattern(self, parameters):
        parameters = self.validate(parameters)
        color = palette()

        width_f = mix(constant(10), scale(10, arc()), constant(parameters.width_factor))

        path = Path(position=line((0, 0), (parameters.length, 0)),
                    direction=constant_direction(0, -1),
                    width=width_f,
                    stroke_alignment=constant(0.5))

        pattern = EmbroideryPattern()

        effects = list(iter(stitch_effects(parameters.stitch_length)))
        offsets = [np.array((0, 30 + i * 15)) for i in range(len(effects))]

        for effect, offset in zip(effects, offsets):
            pattern.add_stitches(effect(path) + offset, next(color))

        return pattern


if __name__ == "__main__":
    Design().cli()
