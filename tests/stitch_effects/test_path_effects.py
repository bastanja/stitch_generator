from itertools import product

import numpy as np
import pytest

from stitch_generator.functions.functions_1d import linear_interpolation
from stitch_generator.stitch_effects.path_effects import (
    contour,
    double_satin,
    double_zigzag,
    lattice,
    meander,
    parallel_stripes,
    satin,
    scribble,
    simple_meander,
    simple_satin,
    simple_stripes,
    simple_zigzag,
    stripes,
    tile_motif,
    variable_underlay,
    zigzag,
)
from stitch_generator.subdivision import subdivide_by_number, subdivision_by_pattern
from stitch_generator.subdivision.subdivide_by_length import regular
from tests.stitch_effects.short_paths import assert_at_least_two_stitches, short_paths

v_motif = np.array(((0, 0), (0.5, 1), (1, 0)), dtype=float)

# returns a single value on short paths
spacing_pattern = subdivision_by_pattern(
    pattern=(0, 0.7), pattern_length=5, alignment=0, offset=0
)

path_effects = {
    "contour": contour(stitch_length=3),
    "double_satin": double_satin(regular(3), regular(3)),
    "double_zigzag": double_zigzag(regular(3)),
    "lattice": lattice(
        strands=3, pattern_f=linear_interpolation(0, 1), pattern_length=10
    ),
    "meander": meander(regular(3), regular(3)),
    "meander_join_ends": meander(regular(3), regular(3), join_ends=True),
    "meander_spacing_pattern": meander(spacing_pattern, regular(3)),
    "parallel_stripes": parallel_stripes(subdivide_by_number(3), regular(3)),
    "satin": satin(regular(3), regular(3)),
    "satin_spacing_pattern": satin(spacing_pattern, regular(3)),
    "scribble": scribble(repetitions=3, line_subdivision=regular(3)),
    "simple_meander": simple_meander(spacing=3, stitch_length=3),
    "simple_satin": simple_satin(spacing=3, stitch_length=3),
    "simple_stripes": simple_stripes(repetitions=3, line_subdivision=regular(3)),
    "simple_zigzag": simple_zigzag(spacing=3),
    "stripes": stripes(subdivide_by_number(3), regular(3)),
    "tile_motif": tile_motif(motif=v_motif, motif_length=10),
    "variable_underlay": variable_underlay(
        stroke_spacing=1, line_subdivision=regular(3)
    ),
    "zigzag": zigzag(regular(3)),
    "zigzag_spacing_pattern": zigzag(spacing_pattern),
}


@pytest.mark.parametrize(
    "effect_name, path_name", list(product(path_effects, short_paths))
)
def test_path_effects_return_points_on_short_paths(effect_name, path_name):
    stitches = path_effects[effect_name](short_paths[path_name])
    assert_at_least_two_stitches(stitches)
