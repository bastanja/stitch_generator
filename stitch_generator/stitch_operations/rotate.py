import numpy as np

from stitch_generator.framework.types import Array2D


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


def rotate_90(stitches: Array2D):
    return rotate_by_sin_cos(stitches, sin=1, cos=0)


def rotate_180(stitches: Array2D):
    return rotate_by_sin_cos(stitches, sin=0, cos=-1)


def rotate_270(stitches: Array2D):
    return rotate_by_sin_cos(stitches, sin=-1, cos=0)
