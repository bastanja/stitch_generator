from typing import Sequence, Tuple

import numpy as np

from stitch_generator.framework.types import Function2D
from stitch_generator.functions.ensure_shape import ensure_1d_shape
from stitch_generator.stitch_operations.rotate import rotate_270


def bezier(control_points: Sequence) -> Tuple[Function2D, Function2D]:
    return bezier_shape(control_points), bezier_direction(control_points)


def bezier_shape(control_points: Sequence) -> Function2D:
    control_points = np.asarray(control_points, dtype=float)

    def f(v):
        points, tangents = de_casteljau(control_points, np.array(v, ndmin=1, dtype=float))
        return points

    return f


def bezier_direction(control_points: Sequence) -> Function2D:
    control_points = np.asarray(control_points, dtype=float)

    def f(v):
        points, tangents = de_casteljau(control_points, np.array(v, ndmin=1, dtype=float))
        return rotate_270(tangents)

    return f


def de_casteljau(control_points: np.ndarray, parameters: np.ndarray) -> (np.ndarray, np.ndarray):
    """
    Subdivides a Bézier curve into segments using De Casteljau's algorithm
    Args:
        control_points: The control points of the Bézier curve
        parameters: The offsets along the curve (between 0 and 1) where the curve is cut into segments
    Returns:
        The points on the curve at the requested offsets
    """
    if len(parameters) == 0:
        return None, None
    interpolated_points = control_points
    parameters = np.atleast_2d(ensure_1d_shape(parameters)).T
    while len(interpolated_points) > 1:
        new_interpolated_points = []
        for i in range(len(interpolated_points) - 1):
            a = interpolated_points[i]
            b = interpolated_points[i + 1]
            vectors = b - a
            interpolated = a + vectors * parameters
            new_interpolated_points.append(interpolated)
        if len(interpolated_points) == 2:
            tangents = vectors
            tangent_lengths = np.linalg.norm(tangents, axis=1, keepdims=True)
            tangents /= tangent_lengths
        interpolated_points = new_interpolated_points

    return interpolated_points[0], tangents
