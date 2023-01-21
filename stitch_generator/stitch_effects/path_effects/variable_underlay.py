import numpy as np

from stitch_generator.framework.path import Path, get_boundaries
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import Array2D, Function1D, SubdivisionFunction
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import multiply, add, subtract, inverse, scale
from stitch_generator.functions.functions_1d import constant, linear_interpolation
from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number
from stitch_generator.subdivision.subdivision_modifiers import remove_end
from stitch_generator.stitch_effects.utilities.range_tree import width_to_level, make_range_tree, \
    tree_to_indices_and_offsets_basic


def variable_underlay(stroke_spacing: float, line_subdivision: SubdivisionFunction) -> StitchEffect:
    return lambda path: variable_underlay_along(path, stroke_spacing=stroke_spacing, line_subdivision=line_subdivision)


def variable_underlay_along(path: Path, stroke_spacing: float, line_subdivision: SubdivisionFunction) -> Array2D:
    # if the shape has no length, return start and end point
    if np.isclose(path.length, 0):
        return path.shape(subdivide_by_number(1))

    pos1 = add(path.shape, multiply(path.direction, multiply(path.width, path.stroke_alignment)))
    width1 = multiply(path.width, path.stroke_alignment)
    path1 = Path(shape=pos1, direction=path.direction, width=width1, stroke_alignment=constant(0))

    pos2 = inverse(add(path.shape,
                       multiply(path.direction, multiply(path.width, subtract(path.stroke_alignment, constant(1))))))
    width2 = inverse(multiply(path.width, subtract(constant(1), path.stroke_alignment)))
    dir2 = inverse(multiply(path.direction, constant(-1)))
    path2 = Path(shape=pos2, direction=dir2, width=width2, stroke_alignment=constant(0))

    step_function = linear_interpolation(0, 1)

    return np.concatenate((_variable_underlay(path1, stroke_spacing, line_subdivision, step_function)[:-1],
                           _variable_underlay(path2, stroke_spacing, line_subdivision, step_function)))


def _variable_underlay(path: Path, stroke_spacing: float, line_subdivision: SubdivisionFunction,
                       step_function: Function1D):
    precision = 10
    segments = int(round(path.length * precision))
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
        path_part = path.split([t1, t2])[1]
        _, baseline = get_boundaries(path_part)
        level_step = add(constant(o1 * stroke_spacing), scale((o2 - o1) * stroke_spacing, step_function))
        direction = multiply(path_part.direction, level_step)
        baseline = add(baseline, direction)
        part_length = estimate_length(baseline)
        stitches.append(baseline(line_subdivision(part_length)))

    stitches.append(baseline(1))
    stitches = np.concatenate(stitches)
    return stitches
