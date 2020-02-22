import numpy as np

from lib.functions_1d import linear_interpolation
from lib.sample import sample


def running_stitch(function, length: float, stitch_length: float, include_last: bool):
    assert stitch_length > 0, "Stitch length must be greater than zero"
    num_stitches = max(int(round(length / stitch_length)), 1)
    return sample(function, num_stitches, include_last)


def running_stitch_line(p1, p2, stitch_length: float, include_last: bool):
    p1 = np.array(p1)
    p2 = np.array(p2)
    distance = np.linalg.norm(p1 - p2)
    return running_stitch(linear_interpolation(p1, p2), distance, stitch_length, include_last)
