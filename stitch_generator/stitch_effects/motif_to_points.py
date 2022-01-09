from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.stitch_effects.utilities.motif_to_points import motif_to_points_along
from stitch_generator.framework.types import SamplingFunction


def motif_to_points(motif_position_sampling: SamplingFunction, line_sampling: SamplingFunction,
                    motif_generator) -> StitchEffect:
    return lambda path: motif_to_points_along(path, motif_position_sampling=motif_position_sampling,
                                              line_sampling=line_sampling, motif_generator=motif_generator)
