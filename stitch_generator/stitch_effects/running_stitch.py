from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.stitch_effects.utilities.running_stitch import running_stitch_along
from stitch_generator.stitch_effects.utilities.variable_running_stitch import variable_running_stitch_along


def running_stitch(stitch_length: float, include_endpoint: bool = True) -> StitchEffect:
    return lambda path: running_stitch_along(path=path, stitch_length=stitch_length, include_endpoint=include_endpoint)


def variable_running_stitch(stitch_length: float, stroke_spacing: float) -> StitchEffect:
    return lambda path: variable_running_stitch_along(path=path, stroke_spacing=stroke_spacing,
                                                      stitch_length=stitch_length)
