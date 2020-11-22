import numpy as np

from tests.functions import all_functions
from stitch_generator.stitch_operations.smooth import smooth


def test_smooth():
    # apply smoothing on samples of 1d and 2d functions
    for name, f in all_functions.items():
        n = 10
        v = np.array([f(t / n) for t in range(n + 1)])
        s = smooth(stitches=v, iterations=5, neighbor_weight=0.5)

        # check that smoothing preserves the start and end stitch
        assert np.allclose(v[0], s[0])
        assert np.allclose(v[-1], s[-1])

        # check that smoothing keeps the number of stitches unchanged.
        assert len(v) == len(s)
