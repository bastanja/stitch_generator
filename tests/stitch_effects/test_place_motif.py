import numpy as np

from stitch_generator.stitch_effects.utilities.place_motif import place_motif_between

v_motif = np.array(((-1, 0), (0, 1), (1, 0)), dtype=float)


def test_place_motif_between_returns_2d_array():
    p1, p2 = np.array((1.0, 2.0)), np.array((3.0, 2.0))
    assert place_motif_between(p1, p1, v_motif).shape == (1, 2)
    assert place_motif_between(p1, p2, np.zeros((0, 2))).shape == (1, 2)
