import numpy as np

from stitch_generator.framework.types import Array2D


def remove_duplicates(points: Array2D, threshold: float = 0.01) -> Array2D:
    """
    Removes duplicate points

    Args:
        points: The points which may contains duplicates
        threshold: The minimal distance between points. Points which are closer to their predecessor than 'threshold'
                   are considered as duplicates and are removed

    Returns:
        The points without duplicates
    """

    to_previous = points - np.roll(points, 1, 0)
    distance_to_previous = np.linalg.norm(to_previous, axis=1)
    long_enough = distance_to_previous > threshold
    return points[long_enough]
