import itertools

import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.functions.functions_1d import linear_interpolation
from stitch_generator.functions.place_motif import place_motif_between
from stitch_generator.utilities.types import SamplingFunction, Array2D


def motif_to_segments_along(path: Path, motif_position_sampling: SamplingFunction, line_sampling: SamplingFunction,
                            motif_generator) -> Array2D:
    length = path.length
    minimal_segment_length = 0.1
    motif_locations = motif_position_sampling(length)

    length_to_param = linear_interpolation(target_low=0, target_high=1, source_low=0, source_high=length)
    sizes = [length_to_param(size) for size in path.width(motif_locations)]

    starts = np.array([max(0, location - size) for location, size in zip(motif_locations, sizes)])
    ends = np.array([min(1, location + size) for location, size in zip(motif_locations, sizes)])

    start_points = path.shape(starts)
    end_points = path.shape(ends)

    motifs = [place_motif_between(start, end, next(motif_generator))[1:] for start, end in zip(start_points, end_points)
              if np.linalg.norm(start - end) > length_to_param(minimal_segment_length)]

    fills = []

    starts = np.append(starts, [1])
    ends = np.append([0], ends)
    spaces = zip(ends, starts)
    for space in spaces:
        difference = space[1] - space[0]
        space_length = difference * length
        samples = line_sampling(space_length) * difference + space[0]
        fills.append(path.shape(samples))

    combined = [i for i in itertools.chain.from_iterable(itertools.zip_longest(fills, motifs)) if i is not None]

    return np.concatenate(combined)
