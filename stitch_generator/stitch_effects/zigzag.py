import numpy as np

from stitch_generator.utilities.types import Function2D, SamplingFunction


def zigzag(boundary_left: Function2D, boundary_right: Function2D, sampling_function: SamplingFunction, length: float):
    p = sampling_function(length)
    if len(p) < 2:
        p = np.array([0, 1], dtype=float)
    stitches = np.zeros((len(p), 2))
    stitches[0::2] = boundary_left(p[0::2])
    stitches[1::2] = boundary_right(p[1::2])
    return stitches


def double_zigzag(boundary_left: Function2D, boundary_right: Function2D, sampling_function: SamplingFunction,
                  length: float):
    points_forward = zigzag(boundary_left, boundary_right, sampling_function, length)
    points_backward = zigzag(boundary_right, boundary_left, sampling_function, length)
    points_backward = np.flipud(points_backward)

    if np.allclose(points_forward[-1], points_backward[0]):
        points_backward = points_backward[1:]

    return np.concatenate((points_forward, points_backward, [points_forward[0]]))
