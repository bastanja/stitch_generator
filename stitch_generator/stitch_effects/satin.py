from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.functions.connect_functions import simple_connect
from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.stitch_effects.utilities.satin import satin_along
from stitch_generator.utilities.types import ConnectFunction, SamplingFunction


def satin(sampling_function: SamplingFunction, connect_function: ConnectFunction) -> StitchEffect:
    return lambda path: satin_along(path=path, sampling_function=sampling_function, connect_function=connect_function)


def simple_satin(spacing: float) -> StitchEffect:
    return lambda path: satin_along(
        path=path, sampling_function=regular(spacing),
        connect_function=simple_connect)
