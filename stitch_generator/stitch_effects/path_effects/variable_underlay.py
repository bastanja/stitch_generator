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
    subtract_functions,
)
from stitch_generator.helpers import get_boundaries
from stitch_generator.subdivision import subdivide_by_number

from ..utilities.range_tree import (
    make_range_tree,
    tree_to_indices_and_offsets_basic,
    width_to_level,
)

# number of samples used to estimate the length of each underlay line,
# the same as the default of estimate_length
_LENGTH_SAMPLES = 100


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

    # The path's area is split along its shape line into two halves, each described by
    # a path that has its shape on the outer boundary and the shape line of the original
    # path as its other boundary. The underlay is stitched forward on the first half and
    # backward on the second half, so that it ends where it started.

    # first half: from the boundary on the positive side to the shape line
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

    # second half: from the boundary on the negative side to the shape line,
    # reversed (inverse) so it runs from the end of the path back to its start, and with
    # flipped direction so that the direction points away from the shape line
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

    # transitions between levels are straight diagonal lines
    step_function = linear_interpolation(0, 1)

    # the last stitch of the first half is the first stitch of the second half
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
    # sample the path finely (precision samples per unit of length), so that changes of
    # the width are located accurately
    precision = 10
    path_length = estimate_length(path.shape)
    segments = int(round(path_length * precision))
    t = subdivide_by_number(number_of_segments=segments)

    # use the smaller width of both ends of each segment, so the underlay stays inside
    widths = path.width(t)
    widths = np.minimum(widths[0:-1], widths[1:])

    # the outermost level (in steps of stroke_spacing from the shape line) that fits
    # into the width of each segment
    levels = width_to_level(widths, stroke_spacing)

    # corner points of the underlay route as (index into t, level)
    width_level_tree = make_range_tree(levels)
    indices, offsets = tree_to_indices_and_offsets_basic(width_level_tree)

    # Consecutive corner points are connected with lines. All lines are evaluated
    # together in a few vectorized calls, as evaluating them one by one is dominated
    # by function call overhead.

    # the second boundary of a path half is the shape line of the original path,
    # i.e. level 0
    _, baseline = get_boundaries(path)

    # start and end of each line, as parameters on the path and as levels;
    # t1 > t2 for lines going backward
    indices = np.asarray(indices)
    offsets = np.asarray(offsets, dtype=float)
    t1, t2 = t[indices[:-1]], t[indices[1:]]
    o1, o2 = offsets[:-1], offsets[1:]
    number_of_lines = len(t1)

    def points(line, u):
        # points at parameters u in [0, 1] along the lines with the given numbers
        s = u * (t2[line] - t1[line]) + t1[line]

        # distance from the shape line along the line, going from level o1 to level o2
        level_step = o1[line] * stroke_spacing + (
            o2[line] - o1[line]
        ) * stroke_spacing * step_function(u)

        # move the line outwards by that distance
        return baseline(s) + path.direction(s) * level_step[:, None]

    # length of each line, sampled like estimate_length does
    samples = np.linspace(0, 1, num=_LENGTH_SAMPLES, endpoint=True)
    line = np.repeat(np.arange(number_of_lines), _LENGTH_SAMPLES)
    sampled = points(line, np.tile(samples, number_of_lines))
    sampled = sampled.reshape(number_of_lines, _LENGTH_SAMPLES, 2)
    lengths = np.linalg.norm(np.diff(sampled, axis=1), axis=2).sum(axis=1)

    # parameters of the stitches along each line
    u = [np.asarray(line_subdivision(length), dtype=float) for length in lengths]
    counts = np.array([len(v) for v in u])
    u = np.concatenate(u)

    # each line leaves out its end point, as it is the start point of the next line
    # (same as remove_end, for all lines at once)
    last = np.cumsum(counts) - 1
    has_end = counts > 0
    has_end[has_end] = np.isclose(u[last[has_end]], 1)
    keep = np.ones(len(u), dtype=bool)
    keep[last[has_end]] = False
    counts = counts - has_end

    # stitches along all lines
    line = np.repeat(np.arange(number_of_lines), counts)
    stitches = points(line, u[keep])

    # add the end point of the last line
    end = points(np.array([number_of_lines - 1]), np.array([1.0]))
    return np.concatenate((stitches, end))
