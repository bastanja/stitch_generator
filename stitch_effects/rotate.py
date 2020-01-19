import math
import numpy as np


def rotate_deg(stitches, angle):
    angle *= math.pi / 180
    c = math.cos(angle)
    s = math.sin(angle)
    return rotate(stitches, c, s)


def rotate(stitches, cos, sin):
    rot = np.array([[cos, sin], [-sin, cos]])
    return np.matmul(stitches, rot)
