import itertools

import numpy as np

from stitch_generator.framework import Array1D, Path, StitchEffect, SubdivisionFunction
from stitch_generator.functions import (
    constant,
    estimate_length,
    inverse,
    mix,
    repeat,
    stairs,
)
from stitch_generator.helpers import get_boundaries, path_is_circular
from stitch_generator.subdivision import (
    alternate_direction,
    remove_end,
    subdivide_by_number,
)


def stripes(
    steps: Array1D, line_subdivision: SubdivisionFunction, step_ratio: float = 0.1
) -> StitchEffect:
    """Creates a stripes stitch effect.

    Parallel lines along the path with intermediate stitches based on a subdivision function. The
    lines are connected at the ends with a step transition.

    Args:
        steps: Array of step values (between 0 and 1) that define the stripe positions.
        line_subdivision: Function that subdivides each zigzag line segment to create
            intermediate stitches.
        step_ratio: Relatvie length of the step transitions along the path. Defaults to 0.1.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.

    Example:
        ```python
        from stitch_generator.subdivision import regular
        from stitch_generator.subdivision import subdivide_by_number
        from stitch_generator.stitch_effects.path_effects import stripes

        effect = stripes(steps=subdivide_by_number(6), line_subdivision=regular(3))
        stitches = effect(path)
        ```
    """
    return lambda path: stripes_along(
        path, steps=steps, line_subdivision=line_subdivision, step_ratio=step_ratio
    )


def simple_stripes(
    repetitions: int, line_subdivision: SubdivisionFunction, step_ratio: float = 0.1
) -> StitchEffect:
    """Creates a simple stripes stitch effect with regular spacing.

    Args:
        repetitions: Number of stripe repetitions.
        line_subdivision: Function that subdivides each zigzag line segment to create
            intermediate stitches.
        step_ratio: Ratio for the step transitions. Defaults to 0.1.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.
    """
    return lambda path: stripes_along(
        path,
        steps=subdivide_by_number(repetitions),
        line_subdivision=line_subdivision,
        step_ratio=step_ratio,
    )


def stripes_along(
    path: Path, steps: Array1D, line_subdivision: SubdivisionFunction, step_ratio: float
):
    """Creates stripes stitches along a path.

    Args:
        path: The path to create stripes stitches along.
        steps: Array of step values (between 0 and 1) that define the stripe positions.
        line_subdivision: Function that subdivides each zigzag line segment to create
            intermediate stitches.
        step_ratio: Ratio for the step transitions.

    Returns:
        Coordinates representing the stripes stitches.
    """
    path_length = estimate_length(path.shape)
    return stripes_between(
        *get_boundaries(path),
        steps=steps,
        line_subdivision=line_subdivision,
        length=path_length,
        step_ratio=step_ratio,
        circular=path_is_circular(path),
    )


def stripes_between(
    boundary_left,
    boundary_right,
    steps: Array1D,
    line_subdivision: SubdivisionFunction,
    length: float,
    step_ratio: float,
    circular: bool,
):
    """Creates stripes stitches between two boundaries.

    Args:
        boundary_left: Function representing the left boundary of the path.
        boundary_right: Function representing the right boundary of the path.
        steps: Array of step values (between 0 and 1) that define the stripe positions.
        line_subdivision: Function that subdivides each zigzag line segment to create
            intermediate stitches.
        length: The length of the path.
        step_ratio: Ratio for the step transitions.
        circular: Whether the path is circular.

    Returns:
        Coordinates representing the stripes stitches.
    """
    repetition_mode = "wrap" if circular else "reflect"
    repetitions = len(steps)
    boundary_left = repeat(r=repetitions, function=boundary_left, mode=repetition_mode)
    boundary_right = repeat(
        r=repetitions, function=boundary_right, mode=repetition_mode
    )

    mix_factor_stairs = stairs(steps, step_ratio)
    mixed = mix(boundary_left, boundary_right, factor=mix_factor_stairs)

    subdivision_length = 1 / repetitions

    line_subdivision = remove_end(line_subdivision)

    t = [
        line_subdivision(length) * subdivision_length + i * subdivision_length
        for i in range(repetitions)
    ]
    t.append([1])
    t = np.concatenate(t)

    return mixed(t)


def parallel_stripes(
    steps: Array1D, line_subdivision: SubdivisionFunction
) -> StitchEffect:
    """Creates a parallel stripes stitch effect.

    Creates parallel lines between the boundaries, alternating direction.

    Args:
        steps: Array of step values (between 0 and 1) that define the stripe positions.
        line_subdivision: Function that subdivides each line to create stitches.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.

    Example:
        ```python
        from stitch_generator.subdivision import regular
        from stitch_generator.subdivision import subdivide_by_number
        from stitch_generator.stitch_effects.path_effects import parallel_stripes

        effect = parallel_stripes(steps=subdivide_by_number(3), line_subdivision=regular(3))
        stitches = effect(path)
        ```
    """
    return lambda path: parallel_stripes_along(path, steps, line_subdivision)


def parallel_stripes_along(
    path: Path, steps: Array1D, line_subdivision: SubdivisionFunction
):
    """Creates parallel stripes stitches along a path.

    Args:
        path: The path to create parallel stripes stitches along.
        steps: Array of step values (between 0 and 1) that define the stripe positions.
        line_subdivision: Function that subdivides each line to create stitches.

    Returns:
        Coordinates representing the parallel stripes stitches.
    """
    path_length = estimate_length(path.shape)
    return parallel_stripes_between(
        *get_boundaries(path),
        length=path_length,
        steps=steps,
        line_subdivision=line_subdivision,
    )


def parallel_stripes_between(
    boundary_left,
    boundary_right,
    length: float,
    steps: Array1D,
    line_subdivision: SubdivisionFunction,
):
    """Creates parallel stripes stitches between two boundaries.

    Args:
        boundary_left: Function representing the left boundary of the path.
        boundary_right: Function representing the right boundary of the path.
        length: The length of the path.
        steps: Array of step values (between 0 and 1) that define the stripe positions.
        line_subdivision: Function that subdivides each line to create stitches.

    Returns:
        Coordinates representing the parallel stripes stitches.
    """
    lines = [mix(boundary_left, boundary_right, constant(t)) for t in steps]
    reverse = itertools.cycle((False, True))
    lines = [inverse(line) if next(reverse) else line for line in lines]
    line_subdivision = alternate_direction(line_subdivision)
    stitch_lines = [line(line_subdivision(length)) for line in lines]
    return np.concatenate(stitch_lines)
