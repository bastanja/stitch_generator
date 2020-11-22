import itertools
from functools import partial

import numpy as np

from stitch_generator.functions.path import Path
from stitch_generator.functions.place_motif import place_motif_at
from stitch_generator.utilities.types import SamplingFunction


def motif_to_points(motif_position_sampling: SamplingFunction, line_sampling: SamplingFunction, motif_generator,
                    length: float):
    return partial(_motif_to_points, motif_position_sampling=motif_position_sampling, line_sampling=line_sampling,
                   motif_generator=motif_generator, length=length)


def _motif_to_points(path: Path, motif_position_sampling: SamplingFunction, line_sampling: SamplingFunction,
                     motif_generator, length):
    motif_locations = motif_position_sampling(length)

    motifs = [place_motif_at(path.position(t), path.direction(t)[0], path.width(t), next(motif_generator)) for
              t in motif_locations]

    fills = []

    spaces = zip(motif_locations, motif_locations[1:])
    for space in spaces:
        difference = space[1] - space[0]
        space_length = difference * length
        samples = line_sampling(space_length) * difference + space[0]
        fills.append(path.position(samples))

    combined = [i for i in itertools.chain.from_iterable(itertools.zip_longest(motifs, fills)) if i is not None]

    return np.concatenate(combined)
