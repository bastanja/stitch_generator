from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.functions.function_modifiers import add, scale, repeat, subtract
from stitch_generator.functions.functions_1d import constant, cosinus, linear_interpolation, arc, smoothstep
from stitch_generator.stitch_effects.utilities.lattice import lattice_along


def lattice(strands, pattern_f, pattern_length) -> StitchEffect:
    return lambda path: lattice_along(path, strands=strands, pattern_f=pattern_f, pattern_length=pattern_length)


_cosine_pattern = add(constant(0.5), scale(0.5, repeat(0.5, cosinus())))
_linear_pattern = linear_interpolation(0, 1)
_peaks = subtract(constant(1), repeat(0.5, arc()))

presets = [
    lattice(strands=3, pattern_f=_cosine_pattern, pattern_length=10),
    lattice(strands=7, pattern_f=_linear_pattern, pattern_length=20),
    lattice(strands=3, pattern_f=_linear_pattern, pattern_length=3),
    lattice(strands=5, pattern_f=_peaks, pattern_length=25),
    lattice(strands=5, pattern_f=smoothstep(), pattern_length=25)
]
