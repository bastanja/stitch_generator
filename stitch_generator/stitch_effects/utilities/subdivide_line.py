import numpy as np

from stitch_generator.shapes.line import line_shape


def subdivide_line(p1, p2, subdivision):
    p1, p2 = np.asarray(p1), np.asarray(p2)
    length = np.linalg.norm(p2 - p1)
    t = subdivision(length)
    return line_shape(p1, p2)(t)
