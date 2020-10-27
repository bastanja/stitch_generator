import numpy as np

from stitch_generator.functions.connect_functions import running_stitch_line
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.path import Path
from stitch_generator.functions.underlay_path import underlay_path
from stitch_generator.stitch_effects.contour import contour_along
from stitch_generator.stitch_effects.satin import double_satin_along


def contour_zigzag_underlay(inset: float, stitch_length: float, zigzag_spacing: float):
    def underlay(path: Path):
        if inset > 0:
            path = underlay_path(path, inset)

        connect_function = running_stitch_line(stitch_length=stitch_length, include_endpoint=False)

        contour = contour_along(path, stitch_length=stitch_length)

        zigzag = double_satin_along(path=path, stitch_spacing=zigzag_spacing, connect_function=connect_function,
                                    length=estimate_length(path.position))

        return np.concatenate((contour, zigzag))

    return underlay
