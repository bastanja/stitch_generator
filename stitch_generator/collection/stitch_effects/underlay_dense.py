import numpy as np

from stitch_generator.collection.sampling.tatami_sampling import tatami_3_1
from stitch_generator.framework.path import Path
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import Array2D
from stitch_generator.functions.get_underlay_path import get_underlay_path
from stitch_generator.sampling.sampling_modifiers import add_start, alternate_direction
from stitch_generator.stitch_effects.path_effects.contour import contour_along
from stitch_generator.stitch_effects.path_effects.variable_underlay import variable_underlay_along


def underlay_dense(inset: float, stitch_length: float, spacing: float) -> StitchEffect:
    def underlay(path: Path) -> Array2D:
        if inset > 0:
            path = get_underlay_path(path, inset)

        contour = contour_along(path, stitch_length=stitch_length)

        fill = variable_underlay_along(path=path, stroke_spacing=spacing,
                                       sampling_function=add_start(alternate_direction(tatami_3_1(stitch_length))))

        return np.concatenate((contour, fill))

    return underlay
