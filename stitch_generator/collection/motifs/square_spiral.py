import itertools

import numpy as np

from stitch_generator.framework.types import Array2D


def square_spiral(level: int, step_size: float) -> Array2D:
    """
    Creates a square spiral motif with a continuous stitch line starting at to bottom left, turning to the middle, then
    turning back to the outer border and ending at the bottom right.

    Args:
        level: The number of turns going inward
        step_size: The distance between the spiral levels

    Returns:
        Stitch coordinates for the square spiral motif, centered around the origin. Width of the motif is
        level * step_size
    """

    # step directions (north, east, south, west)
    directions = (np.array((0, -1)), np.array((1, 0)), np.array((0, 1)), np.array((-1, 0)))

    # steps going inward
    direction_forward = itertools.cycle(directions)
    levels_forward = [level - 1] + [i for i in range(level - 1, 0, -1)] + [1]
    points_forward = _make_steps(levels_forward, direction_forward)

    # steps going outward
    direction_backward = (direction * flip for direction, flip in zip(direction_forward, itertools.cycle((-1, 1))))
    levels_backward = [i for i in range(1, level - 1)] + [level - 1]
    points_backward = _make_steps(levels_backward, direction_backward)

    # calculate start point location
    location = (-level / 2, (level - 1) / 2)

    # concatenate all delta steps
    points = np.concatenate(([location], points_forward, points_backward))

    # convert to point locations
    points = np.cumsum(points, axis=0) * step_size

    return points


def _make_steps(levels, directions):
    points = []
    for level in levels:
        direction = next(directions)
        points += [direction for _ in range(level)]
    return points
