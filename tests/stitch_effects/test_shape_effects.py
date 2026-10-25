import itertools
from itertools import product

import numpy as np
import pytest

from stitch_generator.functions.functions_1d import arc, constant
from stitch_generator.stitch_effects.shape_effects import (
    motif_chain,
    motif_to_points,
    motif_to_segments,
    running_stitch,
    variable_running_stitch,
)
from stitch_generator.subdivision.subdivide_by_length import regular
from stitch_generator.subdivision.subdivision_modifiers import free_end, free_start
from tests.stitch_effects.short_paths import assert_at_least_two_stitches, short_paths

v_motif = np.array(((-1, 0), (0, 1), (1, 0)), dtype=float)

# places no motifs on short paths
sparse_placement = free_start(1, free_end(1, regular(3)))

shape_effects = {
    "motif_chain": motif_chain(
        motif_placement=regular(3),
        motif_generator=itertools.repeat(v_motif),
        motif_rotation_degrees=constant(0),
    ),
    "motif_chain_sparse": motif_chain(
        motif_placement=sparse_placement,
        motif_generator=itertools.repeat(v_motif),
        motif_rotation_degrees=constant(0),
    ),
    "motif_to_points": motif_to_points(
        motif_placement=regular(10),
        line_subdivision=regular(3),
        motif_generator=itertools.repeat(v_motif),
    ),
    "motif_to_points_sparse": motif_to_points(
        motif_placement=sparse_placement,
        line_subdivision=regular(3),
        motif_generator=itertools.repeat(v_motif),
    ),
    "motif_to_segments": motif_to_segments(
        motif_placement=regular(10),
        line_subdivision=regular(3),
        motif_generator=itertools.repeat(v_motif),
        motif_length=2,
    ),
    "running_stitch": running_stitch(stitch_length=3),
    "variable_running_stitch": variable_running_stitch(
        stitch_length=3,
        width_profile=arc,
        min_strokes=1,
        max_strokes=5,
        stroke_spacing=0.3,
    ),
}


@pytest.mark.parametrize(
    "effect_name, path_name", list(product(shape_effects, short_paths))
)
def test_shape_effects_return_points_on_short_paths(effect_name, path_name):
    stitches = shape_effects[effect_name](short_paths[path_name])
    assert_at_least_two_stitches(stitches)
