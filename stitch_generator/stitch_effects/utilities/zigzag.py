import numpy as np

from stitch_generator.framework.types import Function2D, SamplingFunction, Array2D


def zigzag_between(boundary_left: Function2D, boundary_right: Function2D, sampling_function: SamplingFunction,
                   length: float) -> Array2D:
    p = sampling_function(length)
    if len(p) < 2:
        p = boundary_left(0)
    stitches = boundary_left(p)
    stitches[1::2] = boundary_right(p[1::2])
    return stitches


def double_zigzag_between(boundary_left: Function2D, boundary_right: Function2D, sampling_function: SamplingFunction,
                          length: float) -> Array2D:
    points_forward = zigzag_between(boundary_left, boundary_right, sampling_function, length)
    points_backward = zigzag_between(boundary_right, boundary_left, sampling_function, length)

    if np.allclose(points_forward[-1], points_backward[-1]):
        points_backward = points_backward[:-1]

    if np.allclose(points_forward[0], points_backward[0]):
        points_backward = points_backward[1:]

    return np.concatenate((points_forward, np.flipud(points_backward), [points_forward[0]]))
