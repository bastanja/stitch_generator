from typing import Sequence, Tuple

import numpy as np
from scipy.interpolate import interp1d

from stitch_generator.framework.types import CoordinateFunction
from stitch_generator.functions.ensure_shape import ensure_2d_shape
from stitch_generator.functions.functions_2d import constant_direction


def line(
    origin: Sequence[float] = (0, 0), to: Sequence[float] = (100, 0)
) -> Tuple[CoordinateFunction, CoordinateFunction]:
    """Creates a linear path.

    Creates a straight line from the origin point to the destination point.
    The dimension of the line (2D or 3D) is determined by the dimension of
    the origin and destination points.

    Args:
        origin: Starting point of the line. Default is (0, 0) for 2D.
            Can be (x, y) for 2D or (x, y, z) for 3D.
        to: Ending point of the line. Default is (100, 0) for 2D.
            Must have the same dimension as origin.

    Returns:
        A tuple (shape, direction) containing:
        - shape: A function that returns points along the line
        - direction: A function that returns the normalized direction vector
          perpendicular to the line (pointing to the left)

    Example:
        >>> shape, direction = line(origin=(0, 0), to=(100, 0))
        >>> shape(0)  # Returns array([[0., 0.]])
        >>> shape(1)  # Returns array([[100., 0.]])
    """
    shape = line_shape(origin=origin, to=to)
    direction = line_direction(origin=origin, to=to)
    return shape, direction


def line_shape(
    origin: Sequence[float] = (0, 0), to: Sequence[float] = (100, 0)
) -> CoordinateFunction:
    """Creates a function representing a line shape.

    Args:
        origin: Starting point of the line. Can be 2D or 3D.
        to: Ending point of the line. Must have the same dimension as origin.

    Returns:
        A function that returns points along the line. Parameter 0 returns
        the origin, parameter 1 returns the destination.
    """
    interpolation = interp1d(
        np.array([0, 1]), np.vstack((origin, to)), fill_value="extrapolate", axis=0
    )

    def f(v):
        result = interpolation(v)
        return ensure_2d_shape(result)

    return f


def line_direction(
    origin: Sequence[float] = (0, 0), to: Sequence[float] = (100, 0)
) -> CoordinateFunction:
    """Creates a function representing line direction.

    Args:
        origin: Starting point of the line. Can be 2D or 3D.
        to: Ending point of the line. Must have the same dimension as origin.

    Returns:
        A function that returns the normalized direction vector perpendicular
        to the line (pointing to the left). For zero-length lines, returns a
        default direction vector.
    """
    delta = ensure_2d_shape(np.asarray(to) - np.asarray(origin))
    length = np.linalg.norm(delta)
    delta = (delta / length) if length > 0 else delta
    # Rotate 270 degrees clockwise: (x, y) -> (y, -x)
    direction = np.array([[delta[0, 1], -delta[0, 0]]])
    return constant_direction(direction[0][0], direction[0][1])
