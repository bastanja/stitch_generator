import numpy as np

from stitch_generator.framework.types import Array2D
from stitch_generator.stitch_operations.repeat_stitches import repeat_stitches


def add_start_end_stitches(stitches: Array2D, repeated_segments: int = 3) -> Array2D:
    """
    Repeats the start and end stitches two times in order to strengthen the start and end of the seam
    Args:
        stitches: The stitches which should get additional start and end stitches
        repeated_segments: The number of segments which should be repeated (3 means that the last 4 stitches will be repeated)

    Returns:
        The stitches with additional stitches at the start and end
    """
    start_stitches = stitches[0:repeated_segments + 1]
    start = repeat_stitches(start_stitches, times=2)

    end_stitches = stitches[-1:-(repeated_segments + 2):-1]
    end = repeat_stitches(end_stitches, times=2)

    return np.concatenate((start[:-1], stitches, end[1:]))
