import numpy as np

from stitch_generator.stitch_operations.rotate import rotate_90


def calculate_direction(stitches, circular: bool = False):
    """
    Calculates the normal direction for stitches. This is the direction perpendicular to the stitching line at this
    stitch point. From start to end the calculated direction vector points to the left side of the stitch line. The
    length of the direction vectors is always between 1 and 2. For an angle of 90 degrees the length of the direction
    is sqrt(2).
    Requires at least two stitches. Guarantees to return as many directions as the number of stitches.
    """

    # Convert stitches to 2-dimensional numpy array with float values.
    # This makes it possible to pass stitches as lists or tuples with integer values.
    stitches = np.array(stitches, ndmin=2, dtype=float)
    assert len(stitches) > 1, "Direction calculation needs at least two stitches"

    start_is_end = np.all(np.isclose(stitches[0], stitches[-1]))

    prev = np.roll(stitches, 1, axis=0)
    nxt = np.roll(stitches, -1, axis=0)

    if start_is_end:
        prev[0] = prev[-1]
        nxt[-1] = nxt[0]

    # Vectors to the previous and next stitch
    to_previous = _normalize(prev - stitches)
    to_next = _normalize(nxt - stitches)

    # Calculate the normal direction as sum of the vectors to_previous and to_next
    directions = to_next + to_previous

    # If the sum of the vectors to_previous and to_next is smaller than threshold, the stitches are considered
    # as collinear, i.e. the stitch lies in a line with its successor and predecessor.
    threshold = 0.000001
    collinear = np.linalg.norm(directions, axis=1) < threshold

    # For collinear stitches the sum of to_previous and to_next is 0. Therefore, use the perpendicular direction
    # instead
    perpendicular = _get_perpendicular(to_previous)
    directions[collinear] = perpendicular[collinear]

    # Where the length of the direction vector is shorter than 1, normalize it to ensure that the length is at least 1
    too_short = np.linalg.norm(directions, axis=1) < 1
    directions[too_short] = _normalize(directions[too_short])

    # Where the stitch line turns to the right, the direction vector also points to the right. Flip it in order to
    # have all direction vectors point to the left.
    flip = np.sum(perpendicular * to_next, axis=1) < -threshold
    directions[flip] = -directions[flip]

    # For the first and last stitch, use the perpendicular direction as normal direction
    if not circular:
        directions[0] = _get_perpendicular(stitches[0] - stitches[1])
        directions[-1] = _get_perpendicular(stitches[-2] - stitches[-1])

    assert directions.shape == stitches.shape
    return directions


def _get_perpendicular(directions):
    return _normalize(rotate_90(np.array(directions, ndmin=2)))


def _normalize(directions: np.ndarray):
    axis = len(directions.shape) - 1
    return directions / np.linalg.norm(directions, axis=axis, keepdims=True)
