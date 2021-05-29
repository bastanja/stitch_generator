from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.functions.connect_functions import line_with_sampling_function
from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.stitch_effects.utilities.meander import meander_along
from stitch_generator.utilities.types import SamplingFunction


def meander(sampling_function: SamplingFunction, connect_function) -> StitchEffect:
    return lambda path: meander_along(path=path, sampling_function=sampling_function, connect_function=connect_function)


def simple_meander(spacing: float, stitch_length: float) -> StitchEffect:
    return lambda path: meander_along(
        path=path, sampling_function=regular(spacing),
        connect_function=line_with_sampling_function(regular(segment_length=stitch_length)))
