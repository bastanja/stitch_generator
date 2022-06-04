import itertools

import numpy as np

from stitch_generator.collection.stitch_effects.motif_stitches import stem_stitch, e_stitch, three_arrows, arrow_chain, \
    cretan_stitch, feather_stitch, rhomb_motif_stitch, x_motif_stitch, alternating_triangles, chevron_stitch, \
    overlock_stitch
from stitch_generator.framework.embroidery_design import EmbroideryDesign
from stitch_generator.framework.palette import palette
from stitch_generator.framework.parameter import FloatParameter
from stitch_generator.framework.path import Path
from stitch_generator.functions.arc_length_mapping import arc_length_mapping
from stitch_generator.functions.function_modifiers import combine
from stitch_generator.shapes.bezier import bezier, bezier_normals


def bezier_path(control_points):
    shape = bezier(control_points)
    param = arc_length_mapping(shape)
    shape = combine(param, shape)
    direction = combine(param, bezier_normals(control_points))
    return Path(shape=shape, direction=direction)


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="motif_stitches", parameters={
            'stitch_length': FloatParameter("Stitch Length", 2, 3, 6),
            'length': FloatParameter("Length", 10, 95, 200),
            'width': FloatParameter("Width", 0, 15, 50),
            'row_spacing': FloatParameter("Row Spacing", 5, 8, 12),
            'spacing': FloatParameter("Spacing", 2, 2.5, 4),
            'pattern_spacing': FloatParameter("Pattern Spacing", 10, 20, 30)
        })

    def _to_pattern(self, parameters, pattern):
        color = palette()

        effects = [
            stem_stitch(spacing=parameters.spacing, stitch_width=0.6, stitch_length=5, repetitions=5, angle=-25),
            stem_stitch(spacing=parameters.spacing, stitch_width=5, stitch_length=4, repetitions=5, angle=0),
            e_stitch(spacing=parameters.spacing, line_length=4, stitch_length=parameters.stitch_length, angle=45),
            three_arrows(start_end_spacing=parameters.pattern_spacing / 2, pattern_spacing=parameters.pattern_spacing,
                         stitch_length=parameters.stitch_length),
            arrow_chain(spacing=parameters.spacing),
            cretan_stitch(spacing=parameters.spacing, width=0.1, height=3, repetitions=4, zig_zag_height=1),
            cretan_stitch(spacing=parameters.spacing, width=0.1, height=3.5, repetitions=4),
            feather_stitch(spacing=parameters.spacing, width=0, height=3.5, repetitions=2),
            rhomb_motif_stitch(spacing=parameters.spacing, width=4, height=6),
            x_motif_stitch(spacing=parameters.spacing, width=6, height=4),
            alternating_triangles(spacing=parameters.spacing, line_length=4, zig_zag_height=2, repetitions=3),
            overlock_stitch(spacing=parameters.spacing, width=5),
            chevron_stitch(spacing=parameters.spacing, line_length=3, zig_zag_height=2, repetitions=5)
        ]

        y_step = parameters.length / 3
        x = parameters.width
        points = np.array(((0, 0), (y_step, -x), (y_step * 2, x), (y_step * 3, 0)))
        direction = itertools.cycle((False, True))
        init_x = -parameters.length / 2
        init_y = -parameters.row_spacing * (len(effects) - 1) / 2
        offsets = [(init_x, init_y + (i * parameters.row_spacing)) for i in range(len(effects))]
        paths = [bezier_path(points + o) for o in offsets]
        paths = [p if dir else p.inverse() for p, dir in zip(paths, direction)]

        for i, stitch_effect in enumerate(effects):
            pattern.add_stitches(stitch_effect(paths[i]), next(color))


if __name__ == "__main__":
    Design().cli()
