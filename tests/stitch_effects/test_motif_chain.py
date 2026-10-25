import itertools

import numpy as np

from stitch_generator.functions.functions_1d import constant
from stitch_generator.stitch_effects.shape_effects.motif_chain import motif_chain
from tests.paths import line_path

v_motif = ((-1, 0), (0, 1), (1, 0))


def test_motif_chain_without_motif_locations():
    effect = motif_chain(
        motif_placement=lambda _: np.array([]),
        motif_generator=itertools.repeat(np.array(v_motif)),
        motif_rotation_degrees=constant(0),
    )
    stitches = effect(line_path(origin=(10, 0), to=(40, 0)))
    assert np.allclose(stitches, ((10, 0), (40, 0)))
