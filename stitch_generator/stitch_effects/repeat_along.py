import numpy as np

from stitch_generator.functions.function_1d_stairs import stairs
from stitch_generator.functions.function_modifiers import repeat, mix
from stitch_generator.path.get_boundaries import get_boundaries
from stitch_generator.path.path import Path
from stitch_generator.stitch_effects.stitch_effect import StitchEffect
from stitch_generator.utilities.types import SamplingFunction


def repeat_effect(repetitions: int, sampling_function: SamplingFunction, length: float,
                  step_ratio: float) -> StitchEffect:
    return lambda path: repeat_along(path, repetitions=repetitions, sampling_function=sampling_function,
                                     length=length, step_ratio=step_ratio)


def repeat_along(path: Path, repetitions: int, sampling_function: SamplingFunction, length: float, step_ratio: float):
    return repeat_between(*get_boundaries(path), repetitions=repetitions, sampling_function=sampling_function,
                          length=length, step_ratio=step_ratio)


def repeat_between(boundary_left, boundary_right, repetitions: int, sampling_function: SamplingFunction, length: float,
                   step_ratio: float):
    boundary_left = repeat(r=repetitions, function=boundary_left, mode='reflect')
    boundary_right = repeat(r=repetitions, function=boundary_right, mode='reflect')

    mix_factor_stairs = stairs(np.linspace(0, 1, repetitions), step_ratio)
    mixed = mix(boundary_left, boundary_right, factor=mix_factor_stairs)

    sampling_length = 1 / repetitions

    t = [sampling_function(length) * sampling_length + i * sampling_length for i in range(repetitions)]
    t.append([1])
    t = np.concatenate(t)

    return mixed(t)
