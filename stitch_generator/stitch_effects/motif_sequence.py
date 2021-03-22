from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.stitch_effects.utilities.motif_sequence import motif_sequence_along
from stitch_generator.utilities.types import SamplingFunction, Function1D


def motif_sequence(motif_position_sampling: SamplingFunction, motif_generator,
                   motif_rotation_degrees: Function1D) -> StitchEffect:
    return lambda path: motif_sequence_along(path, motif_position_sampling=motif_position_sampling,
                                            motif_generator=motif_generator,
                                            motif_rotation_degrees=motif_rotation_degrees)
