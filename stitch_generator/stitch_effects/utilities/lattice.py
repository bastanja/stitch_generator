from stitch_generator.functions.function_modifiers import add, repeat, multiply
from stitch_generator.functions.get_boundaries import get_boundaries
from stitch_generator.framework.path import Path
from stitch_generator.sampling.sample_by_number import sampling_by_number
from stitch_generator.utilities.types import Array2D


def lattice_along(path: Path, strands, pattern_f, pattern_length) -> Array2D:
    stitch_length = _calculate_stitch_length(pattern_length, strands)
    return _lattice(path=path, strands=strands, length=path.length, pattern_f=pattern_f,
                    pattern_length=pattern_length, stitch_length=stitch_length)


def _lattice(path: Path, strands, length, pattern_f, pattern_length, stitch_length) -> Array2D:
    pattern_repetition = int(round(length / pattern_length))
    times = pattern_repetition * strands + 1

    pattern_f = repeat(times, pattern_f, mode='reflect')
    pattern_f = multiply(pattern_f, repeat(strands, path.width, mode='reflect'))

    left, right = get_boundaries(path)

    repetition_mode = 'wrap' if path.is_circular else 'reflect'
    f = add(repeat(strands, right, mode=repetition_mode),
            multiply(repeat(strands, path.direction, mode=repetition_mode), pattern_f))

    stitches = int(round(pattern_length / stitch_length))
    points = f(sampling_by_number(stitches * times, include_endpoint=True)(1))
    return points


def _calculate_stitch_length(pattern_length, strands, desired_length=2) -> float:
    stitch_length = pattern_length / strands
    times = max(1, int(round(stitch_length / desired_length)))
    stitch_length = stitch_length / times
    return stitch_length
