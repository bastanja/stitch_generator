from functools import partial

import numpy as np

from stitch_generator.design_utilities.embroidery_design import EmbroideryDesign
from stitch_generator.design_utilities.palette import palette
from stitch_generator.design_utilities.parameter import FloatParameter
from stitch_generator.functions.embroidery_pattern import EmbroideryPattern
from stitch_generator.functions.function_modifiers import scale
from stitch_generator.functions.functions_1d import constant, arc
from stitch_generator.functions.functions_2d import bezier, bezier_normals
from stitch_generator.functions.path import Path
from stitch_generator.stitch_effects.lattice import braid, grid, peaks
from itertools import product


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="motif_stitches", parameters={
            'length': FloatParameter("Length", 0.01, 1, 1),
        })

    def get_pattern(self, parameters):
        parameters = self.validate(parameters)
        points = np.array(((0, 0), (30, -20), (70, -20), (100, 0)))
        colors = palette()

        paths = [Path(position=bezier(control_points=points),
                      direction=bezier_normals(control_points=points),
                      width=constant(2),
                      stroke_alignment=constant(0.5)),
                 Path(position=bezier(control_points=points),
                      direction=bezier_normals(control_points=points),
                      width=scale(3, arc()),
                      stroke_alignment=constant(0.5))]

        parts = [path.split([parameters.length])[0] for path in paths]

        stitch_effects = [partial(braid, pattern_length=10),
                          partial(peaks, pattern_length=20),
                          partial(grid, pattern_length=30)]

        pattern = EmbroideryPattern()
        offset = 0
        for path, effect in product(parts, stitch_effects):
            stitches = effect(path)
            stitches = stitches + np.array((0, offset * 20))
            pattern.add_stitches(stitches, next(colors))
            offset += 1

        return pattern


if __name__ == "__main__":
    Design().cli()
