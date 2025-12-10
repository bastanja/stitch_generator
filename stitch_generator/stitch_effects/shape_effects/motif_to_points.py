import itertools

import numpy as np

from stitch_generator.framework import StitchEffect, Coordinates
from stitch_generator.framework import SubdivisionFunction, Array2D, Function2D
from stitch_generator.functions import estimate_length
from ..utilities import place_motif_at
from stitch_generator.subdivision import subdivide_between
from stitch_generator.subdivision import remove_start, remove_end


def motif_to_points(
    motif_placement: SubdivisionFunction,
    line_subdivision: SubdivisionFunction,
    motif_generator,
) -> StitchEffect:
    """Creates a motif-to-points effect that places motifs with intermediate stitches.

    Places a motif at specified positions along the path. Between the motifs, the shape of the
    path is subdivided using a line subdivision function to create intermediate stitches. This
    effect is similar to `motif_chain`, but allows for larger distances between motifs by
    inserting intermediate stitches along the path.

    Args:
        motif_placement: Defines the positions along the path where motifs should be placed.
            This is typically a subdivision function like `regular()` or a pattern-based
            subdivision.
        line_subdivision: Defines how the path segments between motifs should be subdivided
            to create intermediate stitches. Typically `regular(stitch_length)` is used.
        motif_generator: An iterator that yields motifs. Each motif should be a numpy array
            of coordinates. Common generators include `itertools.repeat(motif)` for repeating
            the same motif.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.

    Example:
        ```python
        import itertools
        import numpy as np
        from stitch_generator.subdivision import regular
        from stitch_generator.subdivision import pattern_from_spaces, subdivision_by_pattern
        from stitch_generator.subdivision import free_start, free_end
        from stitch_generator.stitch_effects.shape_effects import motif_to_points

        motif = np.array(((0, 0.0), (3, -3), (0, 0), (-3, -3), (0, 0)))
        pattern = pattern_from_spaces((6, 1, 1, 6), with_start=False, with_end=False)
        motif_placement = subdivision_by_pattern(pattern=pattern, pattern_length=30, alignment=0.5, offset=0)
        motif_placement = free_start(10, free_end(10, motif_placement))

        effect = motif_to_points(
            motif_placement=motif_placement,
            line_subdivision=regular(3),
            motif_generator=itertools.repeat(motif)
        )
        stitches = effect(path)
        ```

    Note:
        - Motifs are **not scaled**. They should have the size which they will have in the
          resulting stitch pattern.
        - Unlike `motif_chain`, this effect fills the gaps between motifs with stitches
          following the path shape, making it suitable for paths with larger gaps between motifs.
    """
    return lambda path: motif_to_points_on_shape(
        path.shape,
        path.direction,
        motif_placement=motif_placement,
        line_subdivision=line_subdivision,
        motif_generator=motif_generator,
    )


def motif_to_points_on_shape(
    shape: Function2D,
    direction: Function2D,
    motif_placement: SubdivisionFunction,
    line_subdivision: SubdivisionFunction,
    motif_generator,
) -> Coordinates:
    """Creates a motif-to-points effect directly on shape and direction functions.

    This is the low-level function that works directly with shape and direction functions,
    without requiring a full Path object.

    Args:
        shape: A CoordinateFunction that defines the center line of the path.
        direction: A CoordinateFunction that defines the direction vectors along the path.
        motif_placement: Defines the positions along the path where motifs should be placed.
        line_subdivision: Defines how the path segments between motifs should be subdivided
            to create intermediate stitches.
        motif_generator: An iterator that yields motifs. Each motif should be a numpy array
            of coordinates.

    Returns:
        An array of stitch coordinates.
    """
    total_length = estimate_length(shape)
    motif_locations = motif_placement(total_length)

    # If there are no motifs, subdivide the whole shape with the line subdivision
    if motif_locations.size == 0:
        return shape(line_subdivision(total_length))

    # place a motif at each motif location along the shape
    motifs = [
        place_motif_at(
            shape(t), direction(t)[0], 1, next(motif_generator), include_endpoint=True
        )
        for t in motif_locations
    ]

    # fill all spaces between the motifs
    inner_subdivision = remove_start(remove_end(line_subdivision))
    fills = [
        shape(subdivide_between(total_length, start, end, inner_subdivision))
        for start, end in zip(motif_locations, motif_locations[1:])
    ]

    # fill the space before the first motif, if there is any
    first_fill = None
    if motif_locations[0] > 0:
        first_fill = shape(
            subdivide_between(
                total_length, 0, motif_locations[0], remove_end(line_subdivision)
            )
        )

    # fill the space after the last motif, if there is any
    last_fill = None
    if motif_locations[-1] < 1:
        last_fill = shape(
            subdivide_between(
                total_length, motif_locations[-1], 1, remove_start(line_subdivision)
            )
        )

    # combine all fills to one list
    fills = [first_fill] + fills + [last_fill]

    # interleave fills and motifs
    combined = [
        i
        for i in itertools.chain.from_iterable(itertools.zip_longest(fills, motifs))
        if i is not None and len(i) > 0
    ]

    return np.concatenate(combined)
