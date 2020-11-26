import numpy as np

from stitch_generator.utilities.types import Array2D


def remove_duplicates(points: Array2D, threshold: float = 0.01):
    to_previous = points - np.roll(points, 1, 0)
    distance_to_previous = np.linalg.norm(to_previous, axis=1)
    long_enough = distance_to_previous > threshold
    return points[long_enough]
