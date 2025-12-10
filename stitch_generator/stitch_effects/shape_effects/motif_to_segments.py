import itertools

import numpy as np

from stitch_generator.framework import StitchEffect, Coordinates
from stitch_generator.framework import SubdivisionFunction, Function2D
from stitch_generator.functions import estimate_length
from stitch_generator.subdivision import (
    free_start,
    free_end,
    remove_start,
    remove_end,
)
from stitch_generator.subdivision import subdivide_between
from stitch_generator.subdivision import subdivide_by_number
from ..utilities import place_motif_between


def motif_to_segments(
    motif_placement: SubdivisionFunction,
    line_subdivision: SubdivisionFunction,
    motif_generator,
    motif_length,
) -> StitchEffect:
    """Creates a motif-to-segments effect that replaces path segments with scaled motifs.

    Places a motif at specified positions along the path. At each motif position, a segment
    of the path is cut out and replaced by the motif. The size of the cut-out segment is
    defined by the `motif_length` parameter. Between the motifs, the shape of the path is
    subdivided using a line subdivision function to create intermediate stitches.

    Args:
        motif_placement: Defines the positions along the path where motifs should be placed
            (these are the center points of the segments to be replaced). This is typically
            a subdivision function like `regular()` or a pattern-based subdivision.
        line_subdivision: Defines how the path segments between motifs should be subdivided
            to create intermediate stitches. Typically `regular(stitch_length)` is used.
        motif_generator: An iterator that yields motifs. Each motif should be a numpy array
            of coordinates. Common generators include `itertools.repeat(motif)` for repeating
            the same motif.
        motif_length: The length of the path segment that will be replaced by each motif.
            The motif will be scaled and rotated to fit this segment.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.

    Example:
        ```python
        import itertools
        from stitch_generator.functions import repeat
        from stitch_generator.subdivision import regular
        from stitch_generator.subdivision import subdivide_by_number
        from stitch_generator.subdivision import free_end, free_start
        from stitch_generator.shapes import circle
        from stitch_generator.stitch_effects.shape_effects import motif_to_segments

        motif = repeat(0.5, circle(radius=7))(subdivide_by_number(8))
        motif_placement = regular(25)
        effect = motif_to_segments(
            motif_placement=motif_placement,
            line_subdivision=regular(3),
            motif_generator=itertools.repeat(motif),
            motif_length=14
        )
        stitches = effect(path)
        ```

    Note:
        - Motifs **are scaled** to fit into the cut-out segments. The original size of the
          motif is not relevant, i.e. it can be in the range [0;1], but does not need to be.
        - The motif must have different start and end points. The motif is scaled and rotated
          so that the start point of the motif lies at the start of the cut-out segment and
          the end point lies at the end of the cut-out segment.
        - The effect automatically keeps the start and end of the path free of motifs to
          ensure only full-length motifs are placed. The `free_start` and `free_end` modifiers
          are applied internally.
    """
    return lambda path: motif_to_segments_on_shape(
        path.shape,
        motif_placement=motif_placement,
        line_subdivision=line_subdivision,
        motif_generator=motif_generator,
        motif_length=motif_length,
    )


def motif_to_segments_on_shape(
    shape: Function2D,
    motif_placement: SubdivisionFunction,
    line_subdivision: SubdivisionFunction,
    motif_generator,
    motif_length,
) -> Coordinates:
    """Creates a motif-to-segments effect directly on a shape function.

    This is the low-level function that works directly with shapefunctions, without requiring a
    full Path object.

    Args:
        shape: A CoordinateFunction that defines the center line of the path.
        motif_placement: Defines the positions along the path where motifs should be placed
            (these are the center points of the segments to be replaced).
        line_subdivision: Defines how the path segments between motifs should be subdivided
            to create intermediate stitches.
        motif_generator: An iterator that yields motifs. Each motif should be a numpy array
            of coordinates.
        motif_length: The length of the path segment that will be replaced by each motif.

    Returns:
        An array of stitch coordinates.
    """
    half_motif_length = motif_length / 2
    # keep start and end free of motifs, to make sure only full length motifs are placed
    motif_placement = free_start(
        half_motif_length, free_end(half_motif_length, motif_placement)
    )

    total_length = estimate_length(shape)

    # if the shape has no length, return start and end point
    if np.isclose(total_length, 0):
        return shape(subdivide_by_number(1))

    # middle positions of the motifs
    motif_locations = motif_placement(total_length)

    # if there is no motif or the motif has no length, subdivide the shape with the line subdivision function
    if len(motif_locations) == 0 or np.isclose(motif_length, 0):
        return shape(line_subdivision(total_length))

    # calculate motif start offsets and end offsets
    relative_motif_length = half_motif_length / total_length
    starts = motif_locations - relative_motif_length
    ends = motif_locations + relative_motif_length

    # evaluate shape at start and end offsets
    start_points = shape(starts)
    end_points = shape(ends)

    # place motifs between start and end points
    motifs = [
        place_motif_between(start, end, next(motif_generator), include_endpoint=True)
        for start, end in zip(start_points, end_points)
    ]

    # avoid start and end points of the line subdivision
    inner_line_subdivision = remove_start(remove_end(line_subdivision))

    starts = np.append(starts, [1])
    ends = np.append([0], ends)

    # fill the gaps between the motifs
    fills = [
        shape(subdivide_between(total_length, s1, s2, inner_line_subdivision))
        for s1, s2 in zip(ends, starts)
    ]

    # interleave the fills and motifs
    combined = [
        i
        for i in itertools.chain.from_iterable(itertools.zip_longest(fills, motifs))
        if i is not None and len(i) > 0
    ]
    combined = [shape(0)] + combined + [shape(1)]

    return np.concatenate(combined)
