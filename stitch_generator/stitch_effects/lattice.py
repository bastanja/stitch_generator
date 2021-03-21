from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.stitch_effects.utilities.lattice import lattice_along


def lattice(strands, pattern_f, pattern_length) -> StitchEffect:
    return lambda path: lattice_along(path, strands=strands, pattern_f=pattern_f, pattern_length=pattern_length)
