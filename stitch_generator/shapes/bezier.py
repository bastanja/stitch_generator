from typing import Sequence

import numpy as np

from stitch_generator.functions.de_casteljau import de_casteljau
from stitch_generator.stitch_operations.rotate import rotate_by_degrees
from stitch_generator.framework.types import Function2D


def bezier(control_points: Sequence) -> Function2D:
    control_points = np.asarray(control_points, dtype=float)

    def f(v):
        points, tangents = de_casteljau(control_points, np.array(v, ndmin=1, dtype=float))
        return points

    return f


def bezier_normals(control_points: Sequence) -> Function2D:
    control_points = np.asarray(control_points, dtype=float)

    def f(v):
        points, tangents = de_casteljau(control_points, np.array(v, ndmin=1, dtype=float))
        return rotate_by_degrees(tangents, -90)

    return f
