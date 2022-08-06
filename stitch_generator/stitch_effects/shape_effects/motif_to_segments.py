import itertools

import numpy as np

from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import SamplingFunction, Array2D, Function2D
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.sampling.sample_by_number import sample_by_number
from stitch_generator.sampling.samples_between import samples_between
from stitch_generator.sampling.sampling_modifiers import free_start, free_end, remove_start, remove_end
from stitch_generator.stitch_effects.utilities.place_motif import place_motif_between


def motif_to_segments(motif_position_sampling: SamplingFunction, line_sampling: SamplingFunction,
                      motif_generator, motif_length) -> StitchEffect:
    return lambda path: motif_to_segments_on_shape(path.shape, motif_position_sampling=motif_position_sampling,
                                                   line_sampling=line_sampling, motif_generator=motif_generator,
                                                   motif_length=motif_length)


def motif_to_segments_on_shape(shape: Function2D, motif_position_sampling: SamplingFunction,
                               line_sampling: SamplingFunction, motif_generator, motif_length) -> Array2D:
    half_motif_length = motif_length / 2
    # keep start and end free of samples, to make sure only full length motifs are placed
    motif_position_sampling = free_start(half_motif_length, free_end(half_motif_length, motif_position_sampling))

    total_length = estimate_length(shape)

    # if the shape has no length, return start and end point
    if np.isclose(total_length, 0):
        return shape(sample_by_number(1))

    # middle positions of the motifs
    motif_locations = motif_position_sampling(total_length)

    # if there is no motif or the motif has no length, sample the shape with the line sampling function
    if len(motif_locations) == 0 or np.isclose(motif_length, 0):
        return shape(line_sampling(total_length))

    # calculate motif start samples and end samples
    relative_motif_length = half_motif_length / total_length
    starts = motif_locations - relative_motif_length
    ends = motif_locations + relative_motif_length

    # evaluate shape at start and end samples
    start_points = shape(starts)
    end_points = shape(ends)

    # place motifs between start and end points
    motifs = [place_motif_between(start, end, next(motif_generator), include_endpoint=True) for start, end in
              zip(start_points, end_points)]

    # avoid start and end points of the line sampling
    inner_line_sampling = remove_start(remove_end(line_sampling))

    starts = np.append(starts, [1])
    ends = np.append([0], ends)

    # fill the gaps between the motifs
    fills = [shape(samples_between(total_length, s1, s2, inner_line_sampling)) for s1, s2 in zip(ends, starts)]

    # interleave the fills and motifs
    combined = [i for i in itertools.chain.from_iterable(itertools.zip_longest(fills, motifs)) if
                i is not None and len(i) > 0]
    combined = [shape(0)] + combined + [shape(1)]

    return np.concatenate(combined)
