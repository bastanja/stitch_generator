import numpy as np


def smooth(stitches: np.ndarray, neighbor_weight: float, iterations: int, circular=False):
    """
    Applies Laplacian smoothing to the stitches, i.e. moves each one closer to the
    center between its predecessor and successor.

    Parameters:
        stitches: The stitches to smooth
        neighbor_weight: Defines how much each stitch is moved to the target in one step.
                         Should be in Range [0;1]
        iterations: Defines how often the smoothing is repeated
        circular: Set to True if the start and end stitch should participate
                  in the smoothing
    """
    assert len(stitches) > 2, "smooth requires at least three stitches"

    closed = np.allclose(stitches[0], stitches[-1])

    # if the first and last stitch are equal, remove the last one
    if circular and closed:
        stitches = stitches[0:-1]

    for _ in range(iterations):

        # move stitches to the right and left by one
        right = np.roll(stitches, 1, 0)
        left = np.roll(stitches, -1, 0)

        if not circular:
            # avoid movement of the start and end stitch by setting the left and
            # right neighbours to the same positions as the start and end stitch
            right[-1] = right[0]
            right[0] = right[1]
            left[0] = left[-1]
            left[-1] = left[-2]

        # target is the center between predecessor and successor
        target = (left + right) / 2
        target -= stitches

        # move stitches closer to the target by the amount defined by neighbor_weight
        stitches += target * neighbor_weight

    # if the first and last stitch were equal, add the last one again
    if circular and closed:
        stitches = np.append(stitches, [stitches[0]], 0)

    return stitches
