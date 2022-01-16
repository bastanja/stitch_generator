import numpy as np

from stitch_generator.functions.functions_1d import linear_interpolation


def scale_motif(motif, min_x: float = 0, min_y: float = 0, max_x: float = 1, max_y: float = 1):
    motif = np.asarray(motif, dtype=float)
    mins = np.min(motif, axis=0)
    maxs = np.max(motif, axis=0)

    scale_x = linear_interpolation(source_low=mins[0], source_high=maxs[0], target_low=min_x, target_high=max_x)
    scale_y = linear_interpolation(source_low=mins[1], source_high=maxs[1], target_low=min_y, target_high=max_y)

    motif[:, 0] = scale_x(motif[:, 0])
    motif[:, 1] = scale_y(motif[:, 1])

    return motif
