import numpy as np

from stitch_generator.framework.types import Array2D


def repeat_stitches(stitches: Array2D, times: int, reflect: bool = True) -> Array2D:
    """
    Repeats a sequence of stitches multiple times.

    Args:
        stitches: The stitches to repeat
        times:    How often to repeat the stitches. In case of odd numbers the end point of the resulting stitch
                  sequence remains the same. In case of even numbers the resulting stitch sequence ends at the start
                  point.
        reflect:  If reflect is True, the stitches are repeated back and forth (start to end, end to start, ...). If
                  reflect is False, the stitches are repeated in the same direction (start to end, start so end, ...).
                  Setting reflect to False is useful for closed shapes like circles.

    Returns:
        The repeated stitches
    """

    # add new axis 0 and repeat the stitches along this axis
    stitch_coordinates = np.repeat(stitches[np.newaxis, :, :], times, axis=0)

    # reverse every second run
    if reflect:
        odd = stitch_coordinates[1::2, :, :]
        odd[:] = np.fliplr(odd)

    # remember the last point of the last run
    last = stitch_coordinates[-1, -1, :]

    # remove end stitch to avoid duplicates
    if reflect:
        stitch_coordinates = stitch_coordinates[:, 0:-1, :]

    # turn grid columns and rows into a single row
    result = stitch_coordinates.reshape((-1, 1, 2), order='C')
    result = result[:, 0]
    if reflect:
        result = np.vstack((result, last))

    return result
