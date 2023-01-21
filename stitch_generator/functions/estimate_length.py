import numpy as np

from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number


def accumulate_lengths(points):
    """
    Calculates the distances between the points and returns the sum of the distances, i.e. the total length of the
    polyline described by the points
    """
    to_previous = points - np.roll(points, 1, 0)
    distance_to_previous = np.linalg.norm(to_previous, axis=1)
    distance_to_previous[0] = 0  # first point has no predecessor, set distance to 0
    accumulated = np.add.accumulate(distance_to_previous)
    return accumulated


def estimate_length(function, number_of_samples=100):
    """
    Approximates the length of a shape function by subdividing it into segments and accumulating the lengths of the
    segments
    Args:
        function: A 2DFunction describing a shape
        number_of_samples: The number of segments used for the subdivision of the shape. More samples increase the
                           accuracy of the length estimation.

    Returns:
        The approximate length ot the function
    """
    samples = subdivide_by_number(number_of_samples)
    lengths = accumulate_lengths(function(samples))
    return lengths[-1]
