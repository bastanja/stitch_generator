from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.stitch_effects.utilities.double_satin import double_satin_along
from stitch_generator.framework.types import ConnectFunction, SamplingFunction


def double_satin(sampling_function: SamplingFunction, connect_function: ConnectFunction) -> StitchEffect:
    return lambda path: double_satin_along(path=path, sampling_function=sampling_function,
                                           connect_function=connect_function)
