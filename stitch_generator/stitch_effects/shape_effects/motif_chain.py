import numpy as np

from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import SubdivisionFunction, Array2D, Function1D, Function2D
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import rotate_degrees
from stitch_generator.stitch_effects.utilities.place_motif import place_motif_at


def motif_chain(motif_placement: SubdivisionFunction, motif_generator,
                motif_rotation_degrees: Function1D) -> StitchEffect:
    return lambda path: motif_chain_on_shape(path.shape, path.direction, motif_placement=motif_placement,
                                             motif_generator=motif_generator,
                                             motif_rotation_degrees=motif_rotation_degrees)


def motif_chain_on_shape(shape: Function2D, direction: Function2D, motif_placement: SubdivisionFunction,
                         motif_generator, motif_rotation_degrees: Function1D) -> Array2D:
    total_length = estimate_length(shape)

    motif_locations = motif_placement(total_length)

    rotation = rotate_degrees(direction, motif_rotation_degrees)
    motifs = [place_motif_at(shape(t), rotation(t)[0], 1, next(motif_generator), include_endpoint=True) for t in
              motif_locations]

    return np.concatenate(motifs)
