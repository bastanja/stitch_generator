import numpy as np

from lib.functions_1d import linear_interpolation, sinus, noise
from lib.functions_2d import circle, line
from stitch_effects.smooth import smooth

def test_smooth():
    # apply smoothing on samples of 1d and 2d functions
    for f in [linear_interpolation(1, 2), sinus(), noise(), circle(), line(10, 20)]:

        n = 10
        v = [f(t/n) for t in range(n+1)]
        s = smooth(v, 0.5, 5)

        # check that smoothing preserves the start and end stitch
        assert np.allclose(v[0], s[0])
        assert np.allclose(v[-1], s[-1])

        # check that smoothing keeps the numer of stitches unchanged.
        assert len(v) == len(s)