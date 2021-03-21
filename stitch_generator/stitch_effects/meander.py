from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.stitch_effects.utilities.meander import meander_along
from stitch_generator.utilities.types import SamplingFunction


def meander(sampling_function: SamplingFunction, connect_function) -> StitchEffect:
    return lambda path: meander_along(path=path, sampling_function=sampling_function, connect_function=connect_function,
                                      length=path.length)
