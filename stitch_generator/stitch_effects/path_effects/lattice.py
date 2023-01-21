from stitch_generator.framework.path import Path, get_boundaries
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import Array2D
from stitch_generator.functions.function_modifiers import add, repeat, multiply
from stitch_generator.subdivision.subdivide_by_number import subdivision_by_number


def lattice(strands, pattern_f, pattern_length) -> StitchEffect:
    return lambda path: lattice_along(path, strands=strands, pattern_f=pattern_f, pattern_length=pattern_length)


def lattice_along(path: Path, strands, pattern_f, pattern_length) -> Array2D:
    stitch_length = _calculate_stitch_length(pattern_length, strands)
    return _lattice(path=path, strands=strands, length=path.length, pattern_f=pattern_f,
                    pattern_length=pattern_length, stitch_length=stitch_length)


def _lattice(path: Path, strands, length, pattern_f, pattern_length, stitch_length) -> Array2D:
    pattern_repetition = int(round(length / pattern_length))
    times = pattern_repetition * strands + 1

    repetition_mode = 'wrap' if path.is_circular else 'reflect'

    pattern_f = repeat(times, pattern_f, mode='reflect')
    pattern_f = multiply(pattern_f, repeat(strands, path.width, mode=repetition_mode))

    left, right = get_boundaries(path)

    f = add(repeat(strands, right, mode=repetition_mode),
            multiply(repeat(strands, path.direction, mode=repetition_mode), pattern_f))

    stitches = int(round(pattern_length / stitch_length))
    points = f(subdivision_by_number(stitches * times)(1))
    return points


def _calculate_stitch_length(pattern_length, strands, desired_length=2) -> float:
    stitch_length = pattern_length / strands
    times = max(1, int(round(stitch_length / desired_length)))
    stitch_length = stitch_length / times
    return stitch_length
