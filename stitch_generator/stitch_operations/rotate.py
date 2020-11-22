import numpy as np

from stitch_generator.functions.ensure_shape import ensure_1d_shape
from stitch_generator.functions.types import Function2D, Function1D, Array2D


def rotate_by_degrees(stitches: Array2D, angle_deg) -> Array2D:
    """
    Rotates stitches around the origin in clockwise direction

    Args:
        stitches:  The stitches to rotate
        angle_deg: The rotation angle in degrees. Can be a single float value or a sequence of values with the same
                   length as 'stitches'

    Returns:
        The rotated stitches
    """
    return rotate_by_radians(stitches, np.deg2rad(angle_deg))


def rotate_by_radians(stitches: Array2D, angle_rad) -> Array2D:
    """
    Rotates stitches around the origin in clockwise direction

    Args:
        stitches:  The stitches to rotate
        angle_rad: The rotation angle in radians. Can be a single float value or a sequence of values with the same
                   length as 'stitches'

    Returns:
        The rotated stitches
    """
    return rotate_by_sin_cos(stitches, np.sin(angle_rad), np.cos(angle_rad))


def rotate_by_sin_cos(stitches: Array2D, sin, cos) -> Array2D:
    """
    Rotates stitches around the origin in clockwise direction

    Args:
        stitches:  The stitches to rotate
        sin:       The sinus of the rotation angle. Can be a single float value or a sequence of values with the same
                   length as 'stitches'
        cos:       The cosinus of the rotation angle. Can be a single float value or a sequence of values with the same
                   length as 'stitches'

    Returns:
        The rotated stitches
    """
    x = stitches[:, 0]
    y = stitches[:, 1]
    return np.array([cos * x - sin * y, sin * x + cos * y]).T


def rotation_by_degrees(stitch_position_function: Function2D, angle_function: Function1D) -> Function2D:
    """
    Creates a rotated 2D Function

    Args:
        stitch_position_function: A 2D Function returning stitch positions
        angle_function:           A 1D Function returning rotation angles in degrees

    Returns:
        A 2D Function that returns the stitches from `stitch_position_function` rotated by the angles from
        `angle_function`
    """
    def f(t):
        t = ensure_1d_shape(t)
        return rotate_by_degrees(stitch_position_function(t), angle_function(t))

    return f


def rotation_by_radians(stitch_position_function: Function2D, angle_function: Function1D) -> Function2D:
    """
    Creates a rotated 2D Function

    Args:
        stitch_position_function: A 2D Function returning stitch positions
        angle_function:           A 1D Function returning rotation angles in radians

    Returns:
        A 2D Function that returns the stitches from `stitch_position_function` rotated by the angles from
        `angle_function`
    """
    def f(t):
        t = ensure_1d_shape(t)
        return rotate_by_radians(stitch_position_function(t), angle_function(t))

    return f
