import numpy as np

from stitch_generator.framework.path import Path, get_boundaries
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import SubdivisionFunction, Array2D
from stitch_generator.functions.ensure_shape import ensure_2d_shape
from stitch_generator.subdivision.subdivide_by_length import regular
from stitch_generator.stitch_effects.utilities.subdivide_line import subdivide_line


def meander(spacing_function: SubdivisionFunction, line_subdivision: SubdivisionFunction,
            join_ends: bool = False) -> StitchEffect:
    return lambda path: meander_along(path=path, spacing_function=spacing_function, line_subdivision=line_subdivision,
                                      join_ends=join_ends)


def simple_meander(spacing: float, stitch_length: float) -> StitchEffect:
    return lambda path: meander_along(path=path, spacing_function=regular(spacing),
                                      line_subdivision=regular(stitch_length), join_ends=False)


def meander_along(path: Path, spacing_function: SubdivisionFunction, line_subdivision: SubdivisionFunction,
                  join_ends: bool = False) -> Array2D:
    return meander_between(*get_boundaries(path), spacing_function=spacing_function, line_subdivision=line_subdivision,
                           join_ends=join_ends, length=path.length)


def meander_between(boundary_left, boundary_right, spacing_function: SubdivisionFunction,
                    line_subdivision: SubdivisionFunction, length: float, join_ends: bool = False) -> Array2D:
    points = _meander(boundary_left, boundary_right, spacing_function=spacing_function, length=length)

    parts = [subdivide_line(points[i - 1], points[i], line_subdivision) for i in range(1, len(points), 2)]

    return _connect_parts(parts, join_ends)


def _connect_parts(parts, join_ends: bool):
    if not join_ends:
        return np.concatenate(parts)

    last_point = None

    def modify_part(part):
        if len(part) == 0:
            return part

        nonlocal last_point

        try:
            part[0] = (part[0] + last_point) / 2
        except TypeError:
            # if last_point was not set yet, ignore it
            pass

        last_point = part[-1]
        return part[:-1]

    return np.concatenate([modify_part(p) for p in parts] + [ensure_2d_shape(last_point)])


def _meander(boundary_left, boundary_right, spacing_function: SubdivisionFunction, length):
    t = spacing_function(length)

    values_left_even = boundary_left(t[0::2])
    values_right_even = boundary_right(t[0::2])
    values_right_odd = boundary_right(t[1::2])
    values_left_odd = boundary_left(t[1::2])

    stitches = np.zeros((len(t) * 2, len(values_left_even[0])))

    stitches[0::4] = values_left_even
    stitches[1::4] = values_right_even
    stitches[2::4] = values_right_odd
    stitches[3::4] = values_left_odd

    return stitches
