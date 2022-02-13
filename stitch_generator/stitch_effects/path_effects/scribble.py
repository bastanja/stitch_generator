import numpy as np

from stitch_generator.framework.path import Path, get_boundaries
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import SamplingFunction
from stitch_generator.functions.function_modifiers import repeat, mix, combine, shift
from stitch_generator.functions.functions_1d import linear_interpolation
from stitch_generator.functions.noise import noise
from stitch_generator.sampling.sampling_modifiers import remove_end


def scribble(repetitions: int, sampling_function: SamplingFunction, noise_scale: float = 1,
             noise_offset: float = 0) -> StitchEffect:
    return lambda path: scribble_along(path, repetitions=repetitions, sampling_function=sampling_function,
                                       noise_scale=noise_scale, noise_offset=noise_offset)


def scribble_along(path: Path, repetitions: int, sampling_function: SamplingFunction, noise_scale: float,
                   noise_offset: float):
    repetition_mode = 'wrap' if path.is_circular else 'reflect'
    return scribble_between(*get_boundaries(path), repetitions=repetitions, sampling_function=sampling_function,
                            length=path.length, noise_scale=noise_scale, noise_offset=noise_offset,
                            repetition_mode=repetition_mode)


def scribble_between(boundary_left, boundary_right, repetitions: int, sampling_function: SamplingFunction,
                     length: float, noise_scale: float, noise_offset: float, repetition_mode: str):
    boundary_left = repeat(r=repetitions, function=boundary_left, mode=repetition_mode)
    boundary_right = repeat(r=repetitions, function=boundary_right, mode=repetition_mode)

    mix_factor = combine(shift(noise_offset, repeat(noise_scale * repetitions * length / 100, noise())),
                         linear_interpolation(target_low=0, target_high=1, source_low=-0.4, source_high=0.4))
    mixed = mix(boundary_left, boundary_right, factor=mix_factor)

    sampling_length = 1 / repetitions

    sampling_function = remove_end(sampling_function)
    t = [sampling_function(length) * sampling_length + i * sampling_length for i in range(repetitions)]
    t.append([1])

    t = np.concatenate(t)

    return mixed(t)
