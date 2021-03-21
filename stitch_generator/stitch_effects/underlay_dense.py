import numpy as np

from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.functions.get_underlay_path import get_underlay_path
from stitch_generator.framework.path import Path
from stitch_generator.stitch_effects.contour import contour_along
from stitch_generator.stitch_effects.utilities.variable_running_stitch import variable_underlay
from stitch_generator.utilities.types import Array2D


def underlay_dense(inset: float, stitch_length: float, spacing: float) -> StitchEffect:
    def underlay(path: Path) -> Array2D:
        if inset > 0:
            path = get_underlay_path(path, inset)

        contour = contour_along(path, stitch_length=stitch_length)

        fill = variable_underlay(path=path, stroke_spacing=spacing, stitch_length=stitch_length)

        return np.concatenate((contour, fill))

    return underlay
