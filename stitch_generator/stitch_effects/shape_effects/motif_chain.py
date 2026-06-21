import numpy as np

from stitch_generator.framework import (
    Coordinates,
    Function1D,
    Function2D,
    StitchEffect,
    SubdivisionFunction,
)
from stitch_generator.functions import ensure_1d_shape, estimate_length
from stitch_generator.stitch_operations import rotate_by_degrees

from ..utilities import place_motif_at


def motif_chain(
    motif_placement: SubdivisionFunction,
    motif_generator,
    motif_rotation_degrees: Function1D,
) -> StitchEffect:
    """Creates a motif chain effect that places motifs along the path.

    Places a motif at specified positions along the path. The motifs are connected by simple
    straight line segments without intermediate stitches. The motifs are rotated so that the
    positive X-axis of the motif points in the same direction as the path direction at the
    location where the motif is placed.

    Args:
        motif_placement: Defines the positions along the path where motifs should be placed.
            This is typically a subdivision function like `regular()` or a pattern-based
            subdivision.
        motif_generator: An iterator that yields motifs. Each motif should be a numpy array
            of coordinates. Common generators include `itertools.repeat(motif)` for repeating
            the same motif, or `repeat_motif_mirrored(motif)` for alternating between a motif
            and its mirrored version.
        motif_rotation_degrees: A function that defines additional rotation in degrees for
            each motif. Use `constant(0)` for no additional rotation, or other functions to
            vary the rotation along the path.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.

    Example:
        ```python
        import numpy as np
        from stitch_generator.functions import constant
        from stitch_generator.helpers import repeat_motif_mirrored
        from stitch_generator.subdivision import regular
        from stitch_generator.stitch_effects.shape_effects import motif_chain

        arrow = np.array(((-3, -2), (0, 0), (3, -2)))
        motif_generator = repeat_motif_mirrored(arrow)
        effect = motif_chain(
            motif_placement=regular(3),
            motif_generator=motif_generator,
            motif_rotation_degrees=constant(0)
        )
        stitches = effect(path)
        ```

    Note:
        - Motifs are **not scaled**. They should have the size which they will have in the
          resulting stitches, i.e. motifs should not be in the range [0;1], but rather
          several millimeters big.
        - The motif is automatically rotated so that its positive X-axis points in the same
          direction as the path direction at the placement location. The `motif_rotation_degrees`
          parameter adds additional rotation on top of this automatic rotation.
        - Motifs are connected by straight line segments without intermediate stitches. For
          paths with large gaps between motifs, this may result in very long stitches.
    """
    return lambda path: motif_chain_on_shape(
        path.shape,
        path.direction,
        motif_placement=motif_placement,
        motif_generator=motif_generator,
        motif_rotation_degrees=motif_rotation_degrees,
    )


def motif_chain_on_shape(
    shape: Function2D,
    direction: Function2D,
    motif_placement: SubdivisionFunction,
    motif_generator,
    motif_rotation_degrees: Function1D,
) -> Coordinates:
    """Creates a motif chain directly on shape and direction functions.

    This is the low-level function that works directly with shape and direction functions,
    without requiring a full Path object.

    Args:
        shape: A CoordinateFunction that defines the center line of the path.
        direction: A CoordinateFunction that defines the direction vectors along the path.
        motif_placement: Defines the positions along the path where motifs should be placed.
        motif_generator: An iterator that yields motifs. Each motif should be a numpy array
            of coordinates.
        motif_rotation_degrees: A function that defines additional rotation in degrees for
            each motif.

    Returns:
        An array of stitch coordinates.
    """
    total_length = estimate_length(shape)

    motif_locations = motif_placement(total_length)

    rotation = _rotate_degrees(direction, motif_rotation_degrees)
    motifs = [
        place_motif_at(
            shape(t), rotation(t)[0], 1, next(motif_generator), include_endpoint=True
        )
        for t in motif_locations
    ]

    return np.concatenate(motifs)


def _rotate_degrees(
    stitch_position_function: Function2D, angle_function: Function1D
) -> Function2D:
    """
    Creates a rotated 2D Function

    Args:
        stitch_position_function: A 2D Function returning stitch positions
        angle_function:           A 1D Function returning rotation angles in degrees

    Returns:
        A 2D Function that returns the stitches from `stitch_position_function` rotated by the angles from
        `angle_function`
    """

    def f(t):
        t = ensure_1d_shape(t)
        return rotate_by_degrees(stitch_position_function(t), angle_function(t))

    return f
