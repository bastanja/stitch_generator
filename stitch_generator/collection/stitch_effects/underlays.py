import numpy as np

from stitch_generator.collection.subdivision.tatami import tatami_3_1
from stitch_generator.framework.path import Path, get_inset_path, inset_sides
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import Array2D
from stitch_generator.subdivision.subdivide_by_length import regular
from stitch_generator.subdivision.subdivision_modifiers import add_start, alternate_direction, remove_end
from stitch_generator.stitch_effects.path_effects.contour import contour_along
from stitch_generator.stitch_effects.path_effects.satin import double_satin_along
from stitch_generator.stitch_effects.path_effects.variable_underlay import variable_underlay_along


def underlay_contour_zigzag(inset: float, stitch_length: float, spacing: float) -> StitchEffect:
    def underlay(path: Path) -> Array2D:
        path = _apply_inset(path, inset)

        contour = contour_along(path, stitch_length=stitch_length)

        zigzag = double_satin_along(path=path, spacing_function=regular(spacing),
                                    line_subdivision=remove_end(regular(segment_length=stitch_length)))

        return np.concatenate((contour[:-1], zigzag))

    return underlay


def underlay_dense(inset: float, stitch_length: float, spacing: float) -> StitchEffect:
    def underlay(path: Path) -> Array2D:
        path = _apply_inset(path, inset)

        contour = contour_along(path, stitch_length=stitch_length)

        fill = variable_underlay_along(path=path, stroke_spacing=spacing,
                                       line_subdivision=add_start(alternate_direction(tatami_3_1(stitch_length))))

        return np.concatenate((contour, fill))

    return underlay


def _apply_inset(path: Path, inset: float) -> Path:
    if inset > 0:
        if path.is_circular:
            path = inset_sides(path, inset)
        else:
            path = get_inset_path(path, inset)
    return path
