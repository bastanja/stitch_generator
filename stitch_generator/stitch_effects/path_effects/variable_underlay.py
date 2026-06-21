import numpy as np

from stitch_generator.framework import (
    Coordinates,
    Function1D,
    Path,
    StitchEffect,
    SubdivisionFunction,
)
from stitch_generator.functions import (
    add_functions,
    constant,
    estimate_length,
    inverse,
    linear_interpolation,
    multiply_functions,
    scale,
    subtract_functions,
)
from stitch_generator.helpers import get_boundaries, split_path
from stitch_generator.subdivision import remove_end, subdivide_by_number

from ..utilities.range_tree import (
    make_range_tree,
    tree_to_indices_and_offsets_basic,
    width_to_level,
)


def variable_underlay(
    stroke_spacing: float, line_subdivision: SubdivisionFunction
) -> StitchEffect:
    """Creates a variable underlay stitch effect.

    A pattern of lines to be used below satin stitches. It raises the satin stitches and gives
    them a firm foundation. The underlay adapts to the width of the path: Where the path is
    wider, there are more repetitions of the underlay. Where the path is narrower, the underlay
    only has fewer repetitions.

    To avoid that the underlay sticks out below the satin stitches, the path for the underlay
    should have a smaller width and be a bit shorter than the path of the Satin stitches. Use
    `stitch_generator.helpers.path_operations.get_inset_path` to create such a Path.

    Args:
        stroke_spacing: The spacing between underlay strokes.
        line_subdivision: Function that subdivides each underlay line to create stitches.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.

    Example:
        ```python
        from stitch_generator.helpers import get_inset_path
        from stitch_generator.subdivision import regular
        from stitch_generator.stitch_effects.path_effects import variable_underlay

        path = get_inset_path(path, inset=1)
        effect = variable_underlay(stroke_spacing=3, line_subdivision=regular(3))
        stitches = effect(path)
        ```
    """
    return lambda path: variable_underlay_along(
        path, stroke_spacing=stroke_spacing, line_subdivision=line_subdivision
    )


def variable_underlay_along(
    path: Path, stroke_spacing: float, line_subdivision: SubdivisionFunction
) -> Coordinates:
    """Creates variable underlay stitches along a path.

    Args:
        path: The path to create variable underlay stitches along.
        stroke_spacing: The spacing between underlay strokes.
        line_subdivision: Function that subdivides each underlay line to create stitches.

    Returns:
        Coordinates representing the variable underlay stitches.
    """
    path_length = estimate_length(path.shape)
    # if the shape has no length, return start and end point
    if np.isclose(path_length, 0):
        return path.shape(subdivide_by_number(1))

    pos1 = add_functions(
        path.shape,
        multiply_functions(
            path.direction, multiply_functions(path.width, path.stroke_alignment)
        ),
    )
    width1 = multiply_functions(path.width, path.stroke_alignment)
    path1 = Path(
        shape=pos1, direction=path.direction, width=width1, stroke_alignment=constant(0)
    )

    pos2 = inverse(
        add_functions(
            path.shape,
            multiply_functions(
                path.direction,
                multiply_functions(
                    path.width, subtract_functions(path.stroke_alignment, constant(1))
                ),
            ),
        )
    )
    width2 = inverse(
        multiply_functions(
            path.width, subtract_functions(constant(1), path.stroke_alignment)
        )
    )
    dir2 = inverse(multiply_functions(path.direction, constant(-1)))
    path2 = Path(shape=pos2, direction=dir2, width=width2, stroke_alignment=constant(0))

    step_function = linear_interpolation(0, 1)

    return np.concatenate(
        (
            _variable_underlay(path1, stroke_spacing, line_subdivision, step_function)[
                :-1
            ],
            _variable_underlay(path2, stroke_spacing, line_subdivision, step_function),
        )
    )


def _variable_underlay(
    path: Path,
    stroke_spacing: float,
    line_subdivision: SubdivisionFunction,
    step_function: Function1D,
) -> Coordinates:
    """Creates variable underlay stitches for a single path side.

    Args:
        path: The path to create variable underlay stitches along.
        stroke_spacing: The spacing between underlay strokes.
        line_subdivision: Function that subdivides each underlay line to create stitches.
        step_function: Function that defines the step pattern along the path.

    Returns:
        Coordinates representing the variable underlay stitches for one side.
    """
    precision = 10
    path_length = estimate_length(path.shape)
    segments = int(round(path_length * precision))
    t = subdivide_by_number(number_of_segments=segments)

    widths = path.width(t)
    widths = np.minimum(widths[0:-1], widths[1:])

    levels = width_to_level(widths, stroke_spacing)

    width_level_tree = make_range_tree(levels)
    indices, offsets = tree_to_indices_and_offsets_basic(width_level_tree)

    line_subdivision = remove_end(line_subdivision)

    stitches = []
    iopairs = list(zip(indices, offsets))
    baseline = path.shape
    for p1, p2 in zip(iopairs, iopairs[1:]):
        i1, o1 = p1
        i2, o2 = p2

        t1, t2 = t[i1], t[i2]
        path_part = split_path(path, [t1, t2])[1]
        _, baseline = get_boundaries(path_part)
        level_step = add_functions(
            constant(o1 * stroke_spacing),
            scale((o2 - o1) * stroke_spacing, step_function),
        )
        direction = multiply_functions(path_part.direction, level_step)
        baseline = add_functions(baseline, direction)
        part_length = estimate_length(baseline)
        stitches.append(baseline(line_subdivision(part_length)))

    stitches.append(baseline(1))
    stitches = np.concatenate(stitches)
    return stitches
