import numpy as np

from stitch_generator.functions.samples import linspace


def accumulate_lengths(points):
    # calculate and accumulate point distances
    to_previous = points - np.roll(points, 1, 0)
    distance_to_previous = np.linalg.norm(to_previous, axis=1)
    distance_to_previous[0] = 0  # first point has no predecessor, set distance to 0
    accumulated = np.add.accumulate(distance_to_previous)
    return accumulated


def estimate_length(function, number_of_samples=100):
    samples = linspace(0, 1, number_of_samples, include_endpoint=True)
    lengths = accumulate_lengths(function(samples))
    return lengths[-1]
