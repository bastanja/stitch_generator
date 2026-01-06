import numpy as np


def subdivide_line(p1, p2, subdivision):
    p1, p2 = np.asarray(p1), np.asarray(p2)
    length = np.linalg.norm(p2 - p1)
    t = subdivision(length)
    # Linear interpolation: p1 + t * (p2 - p1)
    t = np.atleast_1d(t)
    return p1 + t[:, np.newaxis] * (p2 - p1)
