import numpy as np

from stitch_generator.functions.connect_functions import running_stitch_line
from stitch_generator.path.get_underlay_path import get_underlay_path
from stitch_generator.path.path import Path
from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.stitch_effects.contour import contour_along
from stitch_generator.stitch_effects.double_satin import double_satin_along
from stitch_generator.stitch_effects.stitch_effect import StitchEffect
from stitch_generator.stitch_effects.variable_running_stitch import variable_underlay
from stitch_generator.utilities.types import Array2D


def contour_zigzag_underlay(inset: float, stitch_length: float, spacing: float) -> StitchEffect:
    def underlay(path: Path) -> Array2D:
        if inset > 0:
            path = get_underlay_path(path, inset)

        connect_function = running_stitch_line(stitch_length=stitch_length, include_endpoint=False)

        contour = contour_along(path, stitch_length=stitch_length)

        zigzag = double_satin_along(path=path, sampling_function=regular(spacing), connect_function=connect_function,
                                    length=path.length)

        return np.concatenate((contour[:-1], zigzag))

    return underlay


def dense_underlay(inset: float, stitch_length: float, spacing: float) -> StitchEffect:
    def underlay(path: Path) -> Array2D:
        if inset > 0:
            path = get_underlay_path(path, inset)

        contour = contour_along(path, stitch_length=stitch_length)

        fill = variable_underlay(path=path, stroke_spacing=spacing, stitch_length=stitch_length)

        return np.concatenate((contour, fill))

    return underlay
