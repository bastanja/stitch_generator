import itertools

import numpy as np

from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import SamplingFunction, Array2D, Function2D
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.sampling.samples_between import samples_between
from stitch_generator.sampling.sampling_modifiers import remove_start, remove_end
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

    # If there are no motifs, sample the whole shape with the sampling function
    if motif_locations.size == 0:
        return shape(line_sampling(total_length))

    # place a motif at each motif location along the shape
    motifs = [place_motif_at(shape(t), direction(t)[0], 1, next(motif_generator), include_endpoint=True) for t in
              motif_locations]

    # fill all spaces between the motifs
    inner_sampling = remove_start(remove_end(line_sampling))
    fills = [shape(samples_between(total_length, start, end, inner_sampling)) for start, end in
             zip(motif_locations, motif_locations[1:])]

    # fill the space before the first motif, if there is any
    first_fill = None
    if motif_locations[0] > 0:
        first_fill = shape(samples_between(total_length, 0, motif_locations[0], remove_end(line_sampling)))

    # fill the space after the last motif, if there is any
    last_fill = None
    if motif_locations[-1] < 1:
        last_fill = shape(samples_between(total_length, motif_locations[-1], 1, remove_start(line_sampling)))

    # combine all fills to one list
    fills = [first_fill] + fills + [last_fill]

    # interleave fills and motifs
    combined = [i for i in itertools.chain.from_iterable(itertools.zip_longest(fills, motifs)) if i is not None]
    return np.concatenate(combined)
