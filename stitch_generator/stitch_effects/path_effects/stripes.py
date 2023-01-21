import itertools

import numpy as np

from stitch_generator.framework.path import Path, get_boundaries
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import SubdivisionFunction, Array1D
from stitch_generator.functions.function_1d_stairs import stairs
from stitch_generator.functions.function_modifiers import repeat, mix, inverse
from stitch_generator.functions.functions_1d import constant
from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number
from stitch_generator.subdivision.subdivision_modifiers import remove_end, alternate_direction


def stripes(steps: Array1D, line_subdivision: SubdivisionFunction, step_ratio: float = 0.1) -> StitchEffect:
    return lambda path: stripes_along(path, steps=steps, line_subdivision=line_subdivision, step_ratio=step_ratio)


def simple_stripes(repetitions: int, line_subdivision: SubdivisionFunction, step_ratio: float = 0.1) -> StitchEffect:
    return lambda path: stripes_along(path, steps=subdivide_by_number(repetitions), line_subdivision=line_subdivision,
                                      step_ratio=step_ratio)


def stripes_along(path: Path, steps: Array1D, line_subdivision: SubdivisionFunction, step_ratio: float):
    return stripes_between(*get_boundaries(path), steps=steps, line_subdivision=line_subdivision, length=path.length,
                           step_ratio=step_ratio, circular=path.is_circular)


def stripes_between(boundary_left, boundary_right, steps: Array1D, line_subdivision: SubdivisionFunction, length: float,
                    step_ratio: float, circular: bool):
    repetition_mode = 'wrap' if circular else 'reflect'
    repetitions = len(steps)
    boundary_left = repeat(r=repetitions, function=boundary_left, mode=repetition_mode)
    boundary_right = repeat(r=repetitions, function=boundary_right, mode=repetition_mode)

    mix_factor_stairs = stairs(steps, step_ratio)
    mixed = mix(boundary_left, boundary_right, factor=mix_factor_stairs)

    subdivision_length = 1 / repetitions

    line_subdivision = remove_end(line_subdivision)

    t = [line_subdivision(length) * subdivision_length + i * subdivision_length for i in range(repetitions)]
    t.append([1])
    t = np.concatenate(t)

    return mixed(t)


def parallel_stripes(steps: Array1D, line_subdivision: SubdivisionFunction) -> StitchEffect:
    return lambda path: parallel_stripes_along(path, steps, line_subdivision)


def parallel_stripes_along(path: Path, steps: Array1D, line_subdivision: SubdivisionFunction):
    return parallel_stripes_between(*get_boundaries(path), length=path.length, steps=steps,
                                    line_subdivision=line_subdivision)


def parallel_stripes_between(boundary_left, boundary_right, length: float, steps: Array1D,
                             line_subdivision: SubdivisionFunction):
    lines = [mix(boundary_left, boundary_right, constant(t)) for t in steps]
    reverse = itertools.cycle((False, True))
    lines = [inverse(line) if next(reverse) else line for line in lines]
    line_subdivision = alternate_direction(line_subdivision)
    stitch_lines = [line(line_subdivision(length)) for line in lines]
    return np.concatenate(stitch_lines)
