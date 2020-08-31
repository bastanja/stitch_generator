from itertools import product

import numpy as np

from stitch_generator.design_utilities.embroidery_design import EmbroideryDesign
from stitch_generator.design_utilities.palette import palette
from stitch_generator.design_utilities.parameter import FloatParameter
from stitch_generator.functions.embroidery_pattern import EmbroideryPattern
from stitch_generator.functions.function_modifiers import scale
from stitch_generator.functions.function_sequence import function_sequence
from stitch_generator.functions.functions_1d import constant, arc
from stitch_generator.functions.functions_2d import bezier, bezier_normals, line, constant_direction
from stitch_generator.functions.path import Path
from stitch_generator.stitch_effects.lattice import presets


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="lattice", parameters={
            'length': FloatParameter("Length", 0.01, 1, 1),
            'alignment': FloatParameter("Alignment", 0, 0.5, 1),
        })

    def get_pattern(self, parameters):
        parameters = self.validate(parameters)
        points = np.array(((0, 0), (30, -20), (70, 20), (100, 0)))
        colors = palette()

        paths = [Path(position=bezier(control_points=points),
                      direction=bezier_normals(control_points=points),
                      width=constant(10),
                      stroke_alignment=constant(0.5)),
                 Path(position=bezier(control_points=points),
                      direction=bezier_normals(control_points=points),
                      width=scale(12, arc()),
                      stroke_alignment=constant(parameters.alignment))]

        parts = [path.split([parameters.length])[0] for path in paths]

        pattern = EmbroideryPattern()
        offset = 0
        for path, effect in product(parts, presets):
            stitches = effect(path)
            stitches = stitches + np.array((0, offset * 20))
            pattern.add_stitches(stitches, next(colors))
            offset += 1

        return pattern


if __name__ == "__main__":
    Design().cli()