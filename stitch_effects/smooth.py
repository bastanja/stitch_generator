import numpy as np


def smooth(stitches: np.ndarray, neighbor_weight: float, iterations: int):
    """
    Applies Laplacian smoothing to the stitches, i.e. moves each one closer to the
    center between its predecessor and successor.

    Parameters:
        neighbor_weight: Defines how much each stitch is moved to the target in one step.
                         Should be in Range [0;1]
        iterations: Defines how often the smoothing is repeated
    """
    assert len(stitches) > 2, "smooth requires at least three stitches"

    for _ in range(iterations):

        # move stitches to the right and left by one
        right = np.roll(stitches, 1, 0)
        left = np.roll(stitches, -1, 0)

        # set start and end stitches in such a way that they not be moved
        right[-1] = right[0]
        right[0] = right[1]
        left[0] = left[-1]
        left[-1] = left[-2]

        # target is the center between predecessor and successor
        target = (left + right) / 2
        target -= stitches

        # move stitches closer to the target by the amount defined by neighbor_weight
        stitches += target * neighbor_weight

    return stitches

