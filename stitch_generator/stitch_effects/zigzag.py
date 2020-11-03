import numpy as np

from stitch_generator.functions.types import Function2D, SamplingFunction


def zigzag(boundary_left: Function2D, boundary_right: Function2D, sampling_function: SamplingFunction, length: float):
    p = sampling_function(length)
    if len(p) < 2:
        p = np.array([0, 1], dtype=float)
    stitches = np.zeros((len(p), 2))
    stitches[0::2] = boundary_left(p[0::2])
    stitches[1::2] = boundary_right(p[1::2])
    return stitches
