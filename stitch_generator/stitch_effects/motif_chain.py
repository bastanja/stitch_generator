from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.stitch_effects.utilities.motif_chain import motif_chain_along
from stitch_generator.framework.types import SamplingFunction


def motif_chain(motif_position_sampling: SamplingFunction, motif_generator) -> StitchEffect:
    return lambda path: motif_chain_along(path, motif_position_sampling=motif_position_sampling,
                                          motif_generator=motif_generator)
