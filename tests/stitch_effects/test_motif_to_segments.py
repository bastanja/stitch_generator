import itertools

import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.sampling.sample_by_fixed_length import sampling_by_fixed_length
from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.sampling.sampling_modifiers import remove_end, remove_start
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.shape_effects.motif_to_segments import motif_to_segments

v_motif = ((-1, 0), (0, 1), (1, 0))
v_motif_array = np.array(v_motif)


def line_path(origin, to) -> Path:
    shape, direction = line(origin, to)
    return Path(shape=shape, direction=direction)


def do_test(motif_position_sampling, line_sampling, motif_length, line_length):
    motif_generator = itertools.repeat(v_motif)
    path = line_path(origin=(-line_length / 2, 0), to=(line_length / 2, 0))

    effect = motif_to_segments(motif_position_sampling=motif_position_sampling, line_sampling=line_sampling,
                               motif_generator=motif_generator, motif_length=motif_length)

    return effect(path)


def test_motif_to_segments():
    do_test(motif_position_sampling=regular(10), line_sampling=regular(2), motif_length=2, line_length=100)
    do_test(motif_position_sampling=sampling_by_fixed_length(segment_length=10),
            line_sampling=remove_start(remove_end(regular(10))), motif_length=2, line_length=11)
