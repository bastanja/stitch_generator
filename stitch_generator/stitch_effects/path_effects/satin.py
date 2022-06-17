import numpy as np

from stitch_generator.framework.path import Path, get_boundaries
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import Array2D
from stitch_generator.framework.types import Function2D, SamplingFunction
from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.stitch_effects.path_effects.zigzag import zigzag_between, double_zigzag_between
from stitch_generator.stitch_effects.utilities.sample_line import sample_line


def satin(spacing_function: SamplingFunction, line_sampling_function: SamplingFunction) -> StitchEffect:
    return lambda path: satin_along(path=path, spacing_function=spacing_function,
                                    line_sampling_function=line_sampling_function)


def simple_satin(spacing: float, stitch_length: float) -> StitchEffect:
    return lambda path: satin_along(path=path, spacing_function=regular(spacing),
                                    line_sampling_function=regular(stitch_length))


def satin_along(path: Path, spacing_function: SamplingFunction, line_sampling_function: SamplingFunction) -> Array2D:
    return satin_between(*get_boundaries(path), spacing_function=spacing_function,
                         line_sampling_function=line_sampling_function, length=path.length)


def satin_between(boundary_left: Function2D, boundary_right: Function2D, spacing_function: SamplingFunction,
                  line_sampling_function: SamplingFunction, length: float) -> Array2D:
    points = zigzag_between(boundary_left, boundary_right, spacing_function, length)
    connection = [sample_line(*p, line_sampling_function) for p in zip(points, points[1:])]
    connection = connection + [[points[-1]]]
    return np.concatenate(connection)


def double_satin(spacing_function: SamplingFunction, line_sampling_function: SamplingFunction) -> StitchEffect:
    return lambda path: double_satin_along(path=path, spacing_function=spacing_function,
                                           line_sampling_function=line_sampling_function)


def double_satin_along(path: Path, spacing_function: SamplingFunction,
                       line_sampling_function: SamplingFunction) -> Array2D:
    return double_satin_between(*get_boundaries(path), spacing_function=spacing_function,
                                line_sampling_function=line_sampling_function, length=path.length)


def double_satin_between(boundary_left: Function2D, boundary_right: Function2D, spacing_function: SamplingFunction,
                         line_sampling_function: SamplingFunction, length: float) -> Array2D:
    points = double_zigzag_between(boundary_left, boundary_right, spacing_function, length)
    connection = [sample_line(*p, line_sampling_function) for p in zip(points, np.roll(points, -1, 0))]
    return np.concatenate(connection)
