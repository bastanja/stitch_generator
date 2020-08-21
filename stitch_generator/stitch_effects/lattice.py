from functools import partial

from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import scale, add, repeat, multiply, subtract
from stitch_generator.functions.functions_1d import constant, cosinus, linear_interpolation, arc
from stitch_generator.functions.path import Path
from stitch_generator.functions.sample import sample


def lattice(path: Path, strands, pattern_f, pattern_length):
    stitch_length = _calculate_stitch_length(pattern_length, strands)
    return _lattice(path=path, strands=strands, length=estimate_length(path.position), pattern_f=pattern_f,
                    pattern_length=pattern_length, stitch_length=stitch_length)


def _lattice(path: Path, strands, length, pattern_f, pattern_length, stitch_length):
    pattern_repetition = int(round(length / pattern_length))
    times = pattern_repetition * strands + 1

    pattern_f = repeat(times, pattern_f, mode='reflect')
    pattern_f = multiply(pattern_f, repeat(strands, path.width, mode='reflect'))
    f = add(repeat(strands, path.position, mode='reflect'),
            multiply(repeat(strands, path.direction, mode='reflect'), pattern_f))

    stitches = int(round(pattern_length / stitch_length))
    points = sample(f, stitches * times)
    return points


def _calculate_stitch_length(pattern_length, strands, desired_length=2):
    stitch_length = pattern_length / strands
    times = int(round(stitch_length / desired_length))
    stitch_length = stitch_length / times
    return stitch_length


_cosine_pattern = scale(0.5, repeat(0.5, cosinus()))
_linear_pattern = linear_interpolation(0.5, -0.5)
_peaks = subtract(constant(0.5), repeat(0.5, arc()))

braid = partial(lattice, strands=3, pattern_f=scale(5, _cosine_pattern))
grid = partial(lattice, strands=7, pattern_f=scale(5, _linear_pattern))
peaks = partial(lattice, strands=5, pattern_f=scale(5, _peaks))
