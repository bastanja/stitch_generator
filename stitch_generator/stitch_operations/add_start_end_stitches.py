import numpy as np

from stitch_generator.stitch_operations.repeat_stitches import repeat_stitches


def add_start_end_stitches(stitches, count=3):
    start = repeat_stitches(stitches[count:0:-1], times=3)
    end = repeat_stitches(stitches[-1:-count - 1:-1], times=3)
    return np.concatenate((start[:-1], stitches[1:], end[1:]))
