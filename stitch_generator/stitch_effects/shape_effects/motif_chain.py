import numpy as np

from stitch_generator.framework import StitchEffect
from stitch_generator.framework import (
    SubdivisionFunction,
    Array2D,
    Function1D,
    Function2D,
)
from stitch_generator.functions import ensure_1d_shape
from stitch_generator.functions import estimate_length
from ..utilities import place_motif_at
from stitch_generator.stitch_operations import rotate_by_degrees


def motif_chain(
    motif_placement: SubdivisionFunction,
    motif_generator,
    motif_rotation_degrees: Function1D,
) -> StitchEffect:
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
) -> Array2D:
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
