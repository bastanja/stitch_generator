import numpy as np


def roll(points, amount):
    # exclude the first point from the roll operation if it is the same as the last point
    start_index = 1 if np.allclose(points[0], points[-1]) else 0

    # copy is necessary to avoid changing the original points
    modified = points.copy()

    # roll by amount
    modified[start_index::] = np.roll(points[start_index::], amount, axis=0)

    # if the first and last point were equal, make them equal again
    if start_index > 0:
        modified[0] = modified[-1]

    return modified
