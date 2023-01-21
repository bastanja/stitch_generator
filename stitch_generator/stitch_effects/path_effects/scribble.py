import numpy as np

from stitch_generator.framework.path import Path, get_boundaries
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import SubdivisionFunction
from stitch_generator.functions.function_modifiers import repeat, mix, shift
from stitch_generator.functions.noise import noise, fix_distribution
from stitch_generator.subdivision.subdivision_modifiers import remove_end


def scribble(repetitions: int, line_subdivision: SubdivisionFunction, noise_scale: float = 1,
             noise_offset: float = 0) -> StitchEffect:
    return lambda path: scribble_along(path, repetitions=repetitions, line_subdivision=line_subdivision,
                                       noise_scale=noise_scale, noise_offset=noise_offset)


def scribble_along(path: Path, repetitions: int, line_subdivision: SubdivisionFunction, noise_scale: float,
                   noise_offset: float):
    repetition_mode = 'wrap' if path.is_circular else 'reflect'
    return scribble_between(*get_boundaries(path), repetitions=repetitions, line_subdivision=line_subdivision,
                            length=path.length, noise_scale=noise_scale, noise_offset=noise_offset,
                            repetition_mode=repetition_mode)


def scribble_between(boundary_left, boundary_right, repetitions: int, line_subdivision: SubdivisionFunction,
                     length: float, noise_scale: float, noise_offset: float, repetition_mode: str):
    boundary_left = repeat(r=repetitions, function=boundary_left, mode=repetition_mode)
    boundary_right = repeat(r=repetitions, function=boundary_right, mode=repetition_mode)

    noise_function = shift(noise_offset, repeat(noise_scale * repetitions * length / 100, noise()))
    mix_factor = fix_distribution(noise_function, target_low=0)
    mixed = mix(boundary_left, boundary_right, factor=mix_factor)

    subdivision_length = 1 / repetitions

    line_subdivision = remove_end(line_subdivision)
    t = [line_subdivision(length) * subdivision_length + i * subdivision_length for i in range(repetitions)]
    t.append([1])

    t = np.concatenate(t)

    return mixed(t)
