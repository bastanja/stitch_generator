import itertools

import numpy as np

from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import SamplingFunction, Array2D, Function2D
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.stitch_effects.utilities.place_motif import place_motif_at


def motif_to_points(motif_position_sampling: SamplingFunction, line_sampling: SamplingFunction,
                    motif_generator) -> StitchEffect:
    return lambda path: motif_to_points_on_shape(path.shape, path.direction,
                                                 motif_position_sampling=motif_position_sampling,
                                                 line_sampling=line_sampling, motif_generator=motif_generator)


def motif_to_points_on_shape(shape: Function2D, direction: Function2D, motif_position_sampling: SamplingFunction,
                             line_sampling: SamplingFunction, motif_generator) -> Array2D:
    total_length = estimate_length(shape)
    motif_locations = motif_position_sampling(total_length)

    if motif_locations.size > 0:
        motifs = [place_motif_at(shape(t), direction(t)[0], 1, next(motif_generator)) for t in motif_locations]
        starts_with_motif = np.isclose(motif_locations[0], 0)

    else:
        motifs = []
        starts_with_motif = False

    motif_locations = add_first_and_last(motif_locations)

    fills = []
    spaces = zip(motif_locations, motif_locations[1:])
    for space in spaces:
        difference = space[1] - space[0]
        space_length = difference * total_length
        samples = line_sampling(space_length) * difference + space[0]
        fills.append(shape(samples))
    fills.append(shape(1))

    if starts_with_motif:
        parts = itertools.zip_longest(motifs, fills)
    else:
        parts = itertools.zip_longest(fills, motifs)

    combined = [i for i in itertools.chain.from_iterable(parts) if i is not None]

    return np.concatenate(combined)


def add_first_and_last(samples):
    if samples.size == 0:
        return np.array((0.0, 1))
    if not np.isclose(samples[0], 0):
        samples = np.concatenate(([0], samples))
    if not np.isclose(samples[-1], 1):
        samples = np.concatenate((samples, [1]))

    return samples
