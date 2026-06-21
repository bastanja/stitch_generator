import numpy as np

from stitch_generator.framework import (
    CoordinateFunction,
    Path,
    StitchEffect,
    SubdivisionFunction,
)
from stitch_generator.functions import (
    estimate_length,
    fix_distribution,
    mix,
    noise,
    repeat,
    shift,
)
from stitch_generator.helpers import get_boundaries, path_is_circular
from stitch_generator.subdivision import remove_end


def scribble(
    repetitions: int,
    line_subdivision: SubdivisionFunction,
    noise_scale: float = 1,
    noise_offset: float = 0,
) -> StitchEffect:
    """Creates a scribble stitch effect.

    A zigzag line along the Path with random offsets to the side to simulate a hand-drawn scribble
    line.

    Args:
        repetitions: Number of times to repeat the path for the scribble effect.
        line_subdivision: Function that subdivides the path to create stitches.
        noise_scale: Scale factor for the noise function. Defaults to 1.
        noise_offset: Offset for the noise function. Defaults to 0.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.

    Example:
        ```python
        from stitch_generator.collection.subdivision import tatami_3_1
        from stitch_generator.subdivision import alternate_direction, add_start, add_end
        from stitch_generator.stitch_effects.path_effects import scribble

        line_subdivision = alternate_direction(add_start(add_end(tatami_3_1(segment_length=3))))
        effect = scribble(repetitions=4, line_subdivision=line_subdivision, noise_scale=0.25)
        stitches = effect(path)
        ```
    """
    return lambda path: scribble_along(
        path,
        repetitions=repetitions,
        line_subdivision=line_subdivision,
        noise_scale=noise_scale,
        noise_offset=noise_offset,
    )


def scribble_along(
    path: Path,
    repetitions: int,
    line_subdivision: SubdivisionFunction,
    noise_scale: float,
    noise_offset: float,
):
    """Creates scribble stitches along a path.

    Args:
        path: The path to create scribble stitches along.
        repetitions: Number of times to repeat the path for the scribble effect.
        line_subdivision: Function that subdivides the path to create stitches.
        noise_scale: Scale factor for the noise function.
        noise_offset: Offset for the noise function.

    Returns:
        Coordinates representing the scribble stitches.
    """
    repetition_mode = "wrap" if path_is_circular(path) else "reflect"
    path_length = estimate_length(path.shape)
    return scribble_between(
        *get_boundaries(path),
        repetitions=repetitions,
        line_subdivision=line_subdivision,
        length=path_length,
        noise_scale=noise_scale,
        noise_offset=noise_offset,
        repetition_mode=repetition_mode,
    )


def scribble_between(
    boundary_left: CoordinateFunction,
    boundary_right: CoordinateFunction,
    repetitions: int,
    line_subdivision: SubdivisionFunction,
    length: float,
    noise_scale: float,
    noise_offset: float,
    repetition_mode: str,
):
    """Creates scribble stitches between two boundaries.

    Args:
        boundary_left: Function representing the left boundary of the path.
        boundary_right: Function representing the right boundary of the path.
        repetitions: Number of times to repeat the path for the scribble effect.
        line_subdivision: Function that subdivides the path to create stitches.
        length: The length of the path.
        noise_scale: Scale factor for the noise function.
        noise_offset: Offset for the noise function.
        repetition_mode: Mode for repeating boundaries ('wrap' or 'reflect').

    Returns:
        Coordinates representing the scribble stitches.
    """
    boundary_left = repeat(r=repetitions, function=boundary_left, mode=repetition_mode)
    boundary_right = repeat(
        r=repetitions, function=boundary_right, mode=repetition_mode
    )

    noise_function = shift(
        noise_offset, repeat(noise_scale * repetitions * length / 100, noise())
    )
    mix_factor = fix_distribution(noise_function, target_low=0)
    mixed = mix(boundary_left, boundary_right, factor=mix_factor)

    subdivision_length = 1 / repetitions

    line_subdivision = remove_end(line_subdivision)
    t = [
        line_subdivision(length) * subdivision_length + i * subdivision_length
        for i in range(repetitions)
    ]
    t.append([1])

    t = np.concatenate(t)

    return mixed(t)
