from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.stitch_effects.utilities.contour import contour_along


def contour(stitch_length: float) -> StitchEffect:
    return lambda path: contour_along(path, stitch_length=stitch_length)
