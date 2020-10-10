import numpy as np

from stitch_generator.design_utilities.embroidery_design import EmbroideryDesign
from stitch_generator.design_utilities.palette import palette
from stitch_generator.design_utilities.parameter import FloatParameter
from stitch_generator.functions.embroidery_pattern import EmbroideryPattern
from stitch_generator.functions.functions_1d import constant
from stitch_generator.functions.functions_2d import line, constant_direction
from stitch_generator.functions.path import Path
from stitch_generator.stitch_effects.stitch_effect_collection import stitch_effects


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="stitch_effects", parameters={
            'stitch_length': FloatParameter("Stitch length", 1, 3, 6),
            'length': FloatParameter("Length", 10, 80, 200)
        })

    def get_pattern(self, parameters):
        parameters = self.validate(parameters)
        color = palette()

        path = Path(position=line((0, 0), (parameters.length, 0)),
                    direction=constant_direction(0, -1),
                    width=constant(10),
                    stroke_alignment=constant(0.5))

        pattern = EmbroideryPattern()

        effects = list(iter(stitch_effects(parameters.length)))
        offsets = [np.array((0, 30 + i * 15)) for i in range(len(effects))]

        for effect, offset in zip(effects, offsets):
            pattern.add_stitches(effect(path) + offset, next(color))

        return pattern


if __name__ == "__main__":
    Design().cli()
