import itertools

import numpy as np

from stitch_generator.functions.function_modifiers import inverse
from stitch_generator.functions.motif_generators import alternate_direction, repeat_motif
from stitch_generator.functions.place_motif import place_motif_at
from stitch_generator.motifs.leaf import leaf
from stitch_generator.sampling.sample_by_length import regular, sampling_by_length, sample_by_length
from stitch_generator.sampling.sampling_modifiers import free_start_end
from stitch_generator.stitch_effects.utilities.motif_to_points import motif_to_points_along
from stitch_generator.stitch_operations.rotate import rotate_by_degrees


def twig(stem_length: float, leaf_length: float, leaf_width: float, spacing: float, start_length: float,
         end_length: float, stitch_length, angle_left, angle_right):
    motif = repeat_motif(leaf(stem_length=stem_length, leaf_length=leaf_length, leaf_width=leaf_width, angle_degrees=0,
                              stitch_length=stitch_length))

    return twig_with_motif(motif_generator=motif, spacing=spacing, start_length=start_length, end_length=end_length,
                           stitch_length=stitch_length, angle_left=angle_left, angle_right=angle_right)


def twig_with_motif(motif_generator, spacing, start_length, end_length, stitch_length, angle_left, angle_right):
    def f(path):
        alternating_notifs = _cycle_angles(motif_generator, (angle_left, angle_right))
        end_direction = rotate_by_degrees(path.direction(1), 90)[0]
        stitches = [
            motif_to_points_along(path,
                                  motif_position_sampling=free_start_end(start_length, end_length, regular(spacing)),
                                  line_sampling=sampling_by_length(stitch_length, include_endpoint=False),
                                  motif_generator=alternating_notifs)[:-1],
            place_motif_at(path.shape(1), end_direction, 1, next(motif_generator)),
            inverse(path.shape)(sample_by_length(path.length, stitch_length, include_endpoint=True))
        ]
        return np.concatenate(stitches)

    return f


def _cycle_angles(motif_generator, angles):
    angle_gen = itertools.cycle(angles)
    motif_generator = alternate_direction(motif_generator)
    while True:
        yield rotate_by_degrees(next(motif_generator), next(angle_gen))
