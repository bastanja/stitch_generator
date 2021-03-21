from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.stitch_effects.utilities.satin import satin_along
from stitch_generator.utilities.types import ConnectFunction, SamplingFunction


def satin(sampling_function: SamplingFunction, connect_function: ConnectFunction) -> StitchEffect:
    return lambda path: satin_along(path=path, sampling_function=sampling_function, connect_function=connect_function)
