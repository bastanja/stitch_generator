import numpy as np

from stitch_generator.framework.path import Path, get_inset_path
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import Array2D
from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.stitch_effects.path_effects.contour import contour_along
from stitch_generator.stitch_effects.path_effects.satin import double_satin_along


def underlay_contour_zigzag(inset: float, stitch_length: float, spacing: float) -> StitchEffect:
    def underlay(path: Path) -> Array2D:
        if inset > 0:
            path = get_inset_path(path, inset)

        contour = contour_along(path, stitch_length=stitch_length)

        zigzag = double_satin_along(path=path, spacing_function=regular(spacing),
                                    line_sampling_function=regular(segment_length=stitch_length))

        return np.concatenate((contour[:-1], zigzag))

    return underlay
