from stitch_generator.framework.path import Path
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import Coordinates, Function1D
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import (
    add_functions,
    repeat,
    multiply_functions,
)
from stitch_generator.helpers.path_operations import get_boundaries, path_is_circular
from stitch_generator.subdivision.subdivide_by_number import subdivision_by_number


def lattice(strands: int, pattern_f: Function1D, pattern_length: float) -> StitchEffect:
    """Creates a lattice stitch effect.

    A continuous line going back and forth between the left and right boundary of the Path.
    Creates a grid-like pattern.

    Args:
        strands: Number of strands (lines) in the lattice pattern.
        pattern_f: A 1D function that defines the pattern along each strand.
        pattern_length: The length of one pattern repetition.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.

    Example:
        ```python
        from stitch_generator.collection.functions.functions_1d import linear_0_1
        from stitch_generator.stitch_effects.path_effects.lattice import lattice

        effect = lattice(strands=7, pattern_f=linear_0_1, pattern_length=20)
        stitches = effect(path)
        ```

    Note:
        The lattice stitch effect uses a fixed number of stitches for each line from the left to the
        right boundary. Therefore, it may produce very long stitches at locations where the path is
        very wide. Such stitches may not be usable with an embroidery machine. Take care to keep the
        paths narrow enough for the lattice stitch effect.
    """
    return lambda path: lattice_along(
        path, strands=strands, pattern_f=pattern_f, pattern_length=pattern_length
    )


def lattice_along(
    path: Path, strands: int, pattern_f: Function1D, pattern_length: float
) -> Coordinates:
    """Creates lattice stitches along a path.

    Args:
        path: The path to create lattice stitches along.
        strands: Number of strands (lines) in the lattice pattern.
        pattern_f: A 1D function that defines the pattern along each strand.
        pattern_length: The length of one pattern repetition.

    Returns:
        Coordinates representing the lattice stitches.
    """
    stitch_length = _calculate_stitch_length(pattern_length, strands)
    path_length = estimate_length(path.shape)
    return _lattice(
        path=path,
        strands=strands,
        length=path_length,
        pattern_f=pattern_f,
        pattern_length=pattern_length,
        stitch_length=stitch_length,
    )


def _lattice(
    path: Path,
    strands: int,
    length: float,
    pattern_f: Function1D,
    pattern_length: float,
    stitch_length: float,
) -> Coordinates:
    pattern_repetition = int(round(length / pattern_length))
    times = pattern_repetition * strands + 1

    repetition_mode = "wrap" if path_is_circular(path) else "reflect"

    pattern_f = repeat(times, pattern_f, mode="reflect")
    pattern_f = multiply_functions(
        pattern_f, repeat(strands, path.width, mode=repetition_mode)
    )

    left, right = get_boundaries(path)

    f = add_functions(
        repeat(strands, right, mode=repetition_mode),
        multiply_functions(
            repeat(strands, path.direction, mode=repetition_mode), pattern_f
        ),
    )

    stitches = int(round(pattern_length / stitch_length))
    points = f(subdivision_by_number(stitches * times)(1))
    return points


def _calculate_stitch_length(
    pattern_length: float, strands: int, desired_length: float = 2
) -> float:
    """Calculates the stitch length for the lattice pattern.
    Args:
        pattern_length: The length of one pattern repetition.
        strands: Number of strands (lines) in the lattice pattern.
        desired_length: The desired stitch length. Defaults to 2.
    Returns:
        The calculated stitch length.
    """
    stitch_length = pattern_length / strands
    times = max(1, int(round(stitch_length / desired_length)))
    stitch_length = stitch_length / times
    return stitch_length
