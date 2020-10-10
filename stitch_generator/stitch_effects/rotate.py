import numpy as np

from stitch_generator.functions.ensure_shape import ensure_1d_shape


def rotate_deg(stitches, angle_deg):
    return rotate_rad(stitches, np.deg2rad(angle_deg))


def rotate_rad(stitches, angle_rad):
    return rotate(stitches, np.sin(angle_rad), np.cos(angle_rad))


def rotate(stitches, sin, cos):
    x = stitches[:, 0]
    y = stitches[:, 1]
    return np.array([cos * x - sin * y, sin * x + cos * y]).T


def rotate_f_rad(pos, rotation):
    def f(v):
        v = ensure_1d_shape(v)
        return rotate_rad(pos(v), rotation(v))

    return f


def rotate_f_deg(pos, rotation):
    def f(v):
        v = ensure_1d_shape(v)
        return rotate_deg(pos(v), rotation(v))

    return f
