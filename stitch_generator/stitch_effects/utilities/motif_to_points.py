import itertools

import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.functions.place_motif import place_motif_at
from stitch_generator.utilities.types import SamplingFunction, Array2D


def motif_to_points_along(path: Path, motif_position_sampling: SamplingFunction, line_sampling: SamplingFunction,
                          motif_generator) -> Array2D:
    length = path.length
    motif_locations = motif_position_sampling(length)

    motifs = [place_motif_at(path.position(t), path.direction(t)[0], path.width(t), next(motif_generator)) for
              t in motif_locations]

    starts_with_motif = np.isclose(motif_locations[0], 0)

    motif_locations = add_first_and_last(motif_locations)

    fills = []
    spaces = zip(motif_locations, motif_locations[1:])
    for space in spaces:
        difference = space[1] - space[0]
        space_length = difference * length
        samples = line_sampling(space_length) * difference + space[0]
        fills.append(path.position(samples))
    fills.append(path.position(1))

    if starts_with_motif:
        parts = itertools.zip_longest(motifs, fills)
    else:
        parts = itertools.zip_longest(fills, motifs)

    combined = [i for i in itertools.chain.from_iterable(parts) if i is not None]

    return np.concatenate(combined)


def add_first_and_last(samples):
    if not np.isclose(samples[0], 0):
        samples = np.concatenate(([0], samples))
    if not np.isclose(samples[-1], 1):
        samples = np.concatenate((samples, [1]))

    return samples