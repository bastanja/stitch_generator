import itertools
from random import seed, random

import numpy as np

from stitch_generator.framework.embroidery_design import EmbroideryDesign
from stitch_generator.framework.embroidery_pattern import EmbroideryPattern
from stitch_generator.framework.palette import palette
from stitch_generator.framework.parameter import FloatParameter, IntParameter
from stitch_generator.framework.path import Path
from stitch_generator.functions.function_modifiers import repeat, shift
from stitch_generator.functions.functions_1d import linear_interpolation
from stitch_generator.functions.motif_generators import repeat_motif_mirrored, repeat_motif
from stitch_generator.motif_stitches.e_stitch import e_stitch, alternating_e_stitch
from stitch_generator.motif_stitches.stem_stitch import stem_stitch
from stitch_generator.motif_stitches.twig import twig, twig_with_motif
from stitch_generator.motifs.heart import heart
from stitch_generator.motifs.leaf import satin_leaf
from stitch_generator.motifs.line import straight_line_with_motif
from stitch_generator.motifs.satin_circle import satin_circle
from stitch_generator.sampling.sample_by_length import regular, sampling_by_length
from stitch_generator.sampling.sample_by_number import sample_by_number
from stitch_generator.sampling.sampling_modifiers import free_start_end
from stitch_generator.shapes.bezier import bezier, bezier_normals
from stitch_generator.shapes.circle import circle
from stitch_generator.stitch_effects.motif_chain import motif_chain
from stitch_generator.stitch_effects.motif_to_points import motif_to_points
from stitch_generator.stitch_effects.motif_to_segments import motif_to_segments
from stitch_generator.stitch_operations.repeat_stitches import repeat_stitches
from stitch_generator.stitch_operations.rotate import rotate_by_degrees


def arrows():
    half_arrow = np.array(((0, 0.0), (-5, 5), (0, 5), (5, 0)))
    motif_gen = repeat_motif_mirrored(half_arrow)
    return motif_chain(regular(2), motif_gen)


def arrows2():
    single_arrow = np.array(((0, 0.0), (-3, -3), (0, 0), (-3, 3), (0, 0)))
    combined = np.concatenate((single_arrow, single_arrow + (2, 0), single_arrow + (4, 0)))
    return motif_to_segments(
        free_start_end(10, 10, regular(20)), regular(3), repeat_motif(combined))


def lines_with_dots(random_seed):
    seed(random_seed)
    rotate = itertools.cycle((0, 180))
    to_angle = linear_interpolation(-20, 20)
    to_length = linear_interpolation(4, 12)

    def motif_gen():
        while True:
            angle = to_angle(random())
            length = to_length(random())
            stitches = straight_line_with_motif(length=length, stitch_length=3,
                                                motif=satin_circle(2.5, 3, pull_compensation=0.5))
            yield rotate_by_degrees(stitches, angle + next(rotate))

    return motif_to_points(regular(4), sampling_by_length(3, include_endpoint=False), motif_gen())


def star():
    turns = 4
    segments = 11
    radius = 2
    shape = repeat(turns, shift(0.5, circle(radius)), mode='wrap')
    motif = shape(sample_by_number(segments, include_endpoint=True))
    motif += (radius, 0)
    motif = straight_line_with_motif(length=5, stitch_length=3, motif=motif)
    motif_gen = repeat_motif(motif)
    return motif_to_points(regular(10), sampling_by_length(3, include_endpoint=False), motif_gen)


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="motif_stitches", parameters={
            'stitch_spacing': FloatParameter("Stitch spacing", 1, 3, 20),
            'length': FloatParameter("Length", 10, 110, 200),
            'stitch_width': FloatParameter("Stitch Width", 0.1, 0.8, 10),
            'stem_stitch_length': FloatParameter("Stem stitch Length", 1, 4, 15),
            'angle': FloatParameter("Angle", -180, 20, 180),
            'repetitions': IntParameter("Repetitions", 2, 5, 12),
            'leaf_spacing': FloatParameter("Leaf spacing", 3, 7, 15),
            'leaf_angle_left': FloatParameter("Leaf Angle", 0, 45, 90),
            'leaf_angle_right': FloatParameter("Leaf Angle", -90, -45, 0),
            'stitch_length': FloatParameter("Stitch Length", 1, 2, 5),
            'heart_spacing': FloatParameter("Heart spacing", 4, 8, 15),
            'random_seed': IntParameter("Random Seed", 0, 2, 1000),
        })

    def get_pattern(self, parameters):
        parameters = self.validate(parameters)
        color = palette()

        y_step = parameters.length / 3
        x = parameters.length / 4
        control_points = ((0, 0), (y_step, -x), (y_step * 2, x), (y_step * 3, 0))

        path = Path(shape=bezier(control_points), direction=bezier_normals(control_points))

        effects = [
            (0, stem_stitch(
                spacing=parameters.stitch_spacing,
                stitch_width=parameters.stitch_width, stitch_length=parameters.stem_stitch_length,
                repetitions=parameters.repetitions, stitch_rotation=parameters.angle)),
            (10, stem_stitch(
                spacing=2.5,
                stitch_width=5, stitch_length=parameters.stem_stitch_length,
                repetitions=parameters.repetitions, stitch_rotation=0)),
            (14, e_stitch(
                spacing=parameters.stitch_spacing, line_length=parameters.stem_stitch_length,
                stitch_length=parameters.stem_stitch_length, stitch_rotation=parameters.angle)),
            (12, alternating_e_stitch(
                spacing=parameters.stitch_spacing, line_length=parameters.stem_stitch_length,
                stitch_length=parameters.stem_stitch_length, stitch_rotation=0)),
            (16, twig(stem_length=2, leaf_length=7, leaf_width=3, spacing=parameters.leaf_spacing,
                      start_length=parameters.leaf_spacing, end_length=parameters.leaf_spacing,
                      stitch_length=parameters.stitch_length, angle_left=parameters.leaf_angle_left,
                      angle_right=parameters.leaf_angle_right)),
            (21, motif_chain(regular(parameters.heart_spacing),
                             repeat_motif_mirrored(repeat_stitches(heart(parameters.heart_spacing), times=3)))),
            (20, twig_with_motif(spacing=parameters.leaf_spacing, start_length=3,
                                 end_length=parameters.leaf_spacing, stitch_length=parameters.stitch_length,
                                 angle_left=parameters.leaf_angle_left,
                                 angle_right=parameters.leaf_angle_right, motif_generator=
                                 repeat_motif(
                                     satin_leaf(stem_length=5, leaf_length=7, leaf_width=3, angle_degrees=30,
                                                stitch_length=parameters.stitch_length)))),
            (13, arrows()),
            (10, arrows2()),
            (20, lines_with_dots(parameters.random_seed)),
            (25, star())
        ]

        pattern = EmbroideryPattern()

        current_offset = 0
        for i, stitch_effect in enumerate(effects):
            current_offset += stitch_effect[0]
            pattern.add_stitches(stitch_effect[1](path) + (0, current_offset), next(color))

        return pattern


if __name__ == "__main__":
    Design().cli()
