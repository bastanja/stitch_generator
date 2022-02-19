import itertools

import numpy as np

from stitch_generator.framework.path import Path, get_boundaries
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import SamplingFunction, Array1D
from stitch_generator.functions.function_1d_stairs import stairs
from stitch_generator.functions.function_modifiers import repeat, mix, inverse
from stitch_generator.functions.functions_1d import constant
from stitch_generator.sampling.sampling_modifiers import remove_end, alternate_direction


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


def parallel_stripes(steps: Array1D, sampling_function: SamplingFunction) -> StitchEffect:
    return lambda path: parallel_stripes_along(path, steps, sampling_function)


def parallel_stripes_along(path: Path, steps: Array1D, sampling_function: SamplingFunction):
    return parallel_stripes_between(*get_boundaries(path), length=path.length, steps=steps,
                                    sampling_function=sampling_function)


def parallel_stripes_between(boundary_left, boundary_right, length: float, steps: Array1D,
                             sampling_function: SamplingFunction):
    lines = [mix(boundary_left, boundary_right, constant(t)) for t in steps]
    reverse = itertools.cycle((False, True))
    lines = [inverse(line) if next(reverse) else line for line in lines]
    sampling_function = alternate_direction(sampling_function)
    stitch_lines = [line(sampling_function(length)) for line in lines]
    return np.concatenate(stitch_lines)
