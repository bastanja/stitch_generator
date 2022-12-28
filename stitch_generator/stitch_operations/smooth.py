import numpy as np

from stitch_generator.framework.types import Array2D


def smooth(stitches: Array2D, iterations: int, neighbor_weight: float = 0.5, circular=False):
    """
    Applies Laplacian smoothing to the stitches, i.e. moves each one closer to the center between its predecessor and
    successor

    Args:
        stitches:        The stitches to smooth
        iterations:      Defines how often the smoothing is repeated
        neighbor_weight: Defines how much each stitch is moved to the target in one step. Should be in Range [0;1]
        circular:        Set to True if the start and end stitch should participate in the smoothing

    Returns:
        The smoothed stitches
    """
    if len(stitches) < 3:
        return stitches

    # copy is necessary to avoid changing the original stitches
    result = stitches.copy()

    closed = np.allclose(result[0], result[-1])

    # if the first and last stitch are equal, remove the last one
    if circular and closed:
        result = result[0:-1]

    for _ in range(iterations):

        # move stitches to the right and left by one
        right = np.roll(result, 1, 0)
        left = np.roll(result, -1, 0)

        if not circular:
            # avoid movement of the start and end stitch by setting the left and
            # right neighbours to the same positions as the start and end stitch
            right[-1] = right[0]
            right[0] = right[1]
            left[0] = left[-1]
            left[-1] = left[-2]

        # target is the center between predecessor and successor
        target = (left + right) / 2
        target -= result

        # move stitches closer to the target by the amount defined by neighbor_weight
        result += target * neighbor_weight

    # if the first and last stitch were equal, add the last one again
    if circular and closed:
        result = np.append(result, [result[0]], 0)

    return result
