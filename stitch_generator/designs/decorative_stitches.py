import itertools

import numpy as np

from stitch_generator.collection.stitch_effects.decorative_stitches import stem_stitch, e_stitch, three_arrows, \
    arrow_chain, cretan_stitch, feather_stitch, rhomb_motif_stitch, x_motif_stitch, alternating_triangles, \
    chevron_stitch, overlock_stitch
from stitch_generator.framework.embroidery_design import EmbroideryDesign
from stitch_generator.framework.palette import palette
from stitch_generator.framework.parameter import FloatParameter
from stitch_generator.framework.path import Path
from stitch_generator.functions.arc_length_mapping import arc_length_mapping
from stitch_generator.functions.function_modifiers import chain
from stitch_generator.shapes.bezier import bezier, bezier_normals


def bezier_path(control_points):
    shape = bezier(control_points)
    param = arc_length_mapping(shape)
    shape = chain(param, shape)
    direction = chain(param, bezier_normals(control_points))
    return Path(shape=shape, direction=direction)


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="decorative_stitches", parameters={
            'length': FloatParameter("Length", 10, 95, 200),
            'curve_width': FloatParameter("Curve Width", 0, 15, 50),
            'row_spacing': FloatParameter("Row Spacing", 7, 10, 14),
            'spacing': FloatParameter("Spacing", 2, 2.5, 4),
            'pattern_spacing': FloatParameter("Pattern Spacing", 10, 20, 30),
            'stitch_width': FloatParameter("Stitch width", 3, 5, 10)
        })

    def _to_pattern(self, parameters, pattern):
        color = palette()

        effects = [
            alternating_triangles(spacing=parameters.spacing, line_length=4, width=parameters.stitch_width,
                                  repetitions=3),
            arrow_chain(arrow_width=parameters.stitch_width, arrow_length=2, arrow_spacing=parameters.spacing),
            chevron_stitch(spacing=parameters.spacing * 2, line_length=3, width=parameters.stitch_width, repetitions=5),
            cretan_stitch(spacing=parameters.spacing * 2, stitch_width=0.1, stitch_length=3, repetitions=4,
                          zigzag_width=2),
            cretan_stitch(spacing=parameters.spacing * 2, stitch_width=0.1, stitch_length=3.5, repetitions=4),
            e_stitch(spacing=parameters.spacing, line_length=4, stitch_length=10, angle=45),
            feather_stitch(spacing=parameters.spacing, stitch_width=0, stitch_length=3.5, repetitions=2),
            overlock_stitch(length=parameters.spacing, width=parameters.stitch_width),
            rhomb_motif_stitch(spacing=parameters.spacing, width=parameters.stitch_width, length=4),
            stem_stitch(spacing=parameters.spacing, stitch_width=0.6, stitch_length=5, repetitions=5, angle=-25),
            stem_stitch(spacing=parameters.spacing, stitch_width=parameters.stitch_width, stitch_length=4,
                        repetitions=5, angle=0),
            three_arrows(arrow_spacing=2, group_spacing=parameters.pattern_spacing,
                         start_end_spacing=parameters.pattern_spacing / 2, stitch_length=3),
            x_motif_stitch(spacing=parameters.spacing, width=parameters.stitch_width, length=4)
        ]

        y_step = parameters.length / 3
        x = parameters.curve_width
        points = np.array(((0, 0), (y_step, -x), (y_step * 2, x), (y_step * 3, 0)))
        direction = itertools.cycle((True, False))
        init_x = -parameters.length / 2
        init_y = -parameters.row_spacing * (len(effects) - 1) / 2
        offsets = [(init_x, init_y + (i * parameters.row_spacing)) for i in range(len(effects))]
        paths = [bezier_path(points + o) for o in offsets]
        paths = [p if dir else p.inverse() for p, dir in zip(paths, direction)]

        for i, stitch_effect in enumerate(effects):
            pattern.add_stitches(stitch_effect(paths[i]), next(color))


if __name__ == "__main__":
    Design().cli()
