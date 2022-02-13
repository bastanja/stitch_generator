import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import SamplingFunction
from stitch_generator.functions.function_1d_stairs import stairs
from stitch_generator.functions.function_modifiers import repeat, mix
from stitch_generator.functions.get_boundaries import get_boundaries
from stitch_generator.sampling.sampling_modifiers import remove_end


def stripes(repetitions: int, sampling_function: SamplingFunction, step_ratio: float = 0.1) -> StitchEffect:
    return lambda path: stripes_along(path, repetitions=repetitions, sampling_function=sampling_function,
                                      step_ratio=step_ratio)


def stripes_along(path: Path, repetitions: int, sampling_function: SamplingFunction, step_ratio: float):
    return stripes_between(*get_boundaries(path), repetitions=repetitions, sampling_function=sampling_function,
                           length=path.length, step_ratio=step_ratio, circular=path.is_circular)


def stripes_between(boundary_left, boundary_right, repetitions: int, sampling_function: SamplingFunction, length: float,
                    step_ratio: float, circular: bool):
    repetition_mode = 'wrap' if circular else 'reflect'
    boundary_left = repeat(r=repetitions, function=boundary_left, mode=repetition_mode)
    boundary_right = repeat(r=repetitions, function=boundary_right, mode=repetition_mode)

    mix_factor_stairs = stairs(np.linspace(0, 1, repetitions), step_ratio)
    mixed = mix(boundary_left, boundary_right, factor=mix_factor_stairs)

    sampling_length = 1 / repetitions

    sampling_function = remove_end(sampling_function)

    t = [sampling_function(length) * sampling_length + i * sampling_length for i in range(repetitions)]
    t.append([1])
    t = np.concatenate(t)

    return mixed(t)