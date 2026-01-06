from typing import Sequence, Tuple

import numpy as np

from stitch_generator.framework.types import CoordinateFunction
from stitch_generator.functions.ensure_shape import ensure_1d_shape


def bezier(control_points: Sequence) -> Tuple[CoordinateFunction, CoordinateFunction]:
    """Creates a Bézier curve path.

    Creates a Bézier curve from the given control points. Supports quadratic
    (3 points), cubic (4 points), or higher-degree curves. The dimension of the
    curve (2D or 3D) is determined by the dimension of the control points.

    Args:
        control_points: A sequence of coordinate points. Must have at least
            2 points. The curve passes through the first and last points and is
            influenced by the intermediate control points. Each point should have
            the same dimension (2D or 3D).

    Returns:
        A tuple (shape, direction) containing:
        - shape: A function that returns points on the Bézier curve
        - direction: A function that returns normalized direction vectors
          perpendicular to the curve (pointing to the left)

    Example:
        >>> # Cubic Bézier curve (2D)
        >>> points = [(0, 0), (25, 50), (75, -50), (100, 0)]
        >>> shape, direction = bezier(points)
        >>> shape(0)  # Returns array([[0., 0.]])
        >>> shape(1)  # Returns array([[100., 0.]])
    """
    return bezier_shape(control_points), bezier_direction(control_points)


def bezier_shape(control_points: Sequence) -> CoordinateFunction:
    """Creates a function representing a Bézier curve shape.

    Args:
        control_points: A sequence of coordinate points. Must have at least 2.
            The dimension of the points (2D or 3D) determines the dimension
            of the returned function.

    Returns:
        A function that returns points on the Bézier curve. Parameter 0 returns
        the first control point, parameter 1 returns the last control point.
    """
    control_points = np.asarray(control_points, dtype=float)

    def f(v):
        points, tangents = de_casteljau(control_points, np.array(v, ndmin=1, dtype=float))
        return points

    return f


def bezier_direction(control_points: Sequence) -> CoordinateFunction:
    """Creates a function representing Bézier curve direction.

    Args:
        control_points: A sequence of coordinate points. Must have at least 2.
            The dimension of the points determines the dimension of the returned
            function.

    Returns:
        A function that returns normalized direction vectors perpendicular to
        the curve (rotated 270 degrees from the tangent).
    """
    control_points = np.asarray(control_points, dtype=float)

    def f(v):
        points, tangents = de_casteljau(control_points, np.array(v, ndmin=1, dtype=float))
        # Rotate 270 degrees clockwise: (x, y) -> (y, -x)
        return np.column_stack([tangents[:, 1], -tangents[:, 0]])

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
