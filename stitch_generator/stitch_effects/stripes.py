from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.stitch_effects.utilities.stripes import stripes_along
from stitch_generator.utilities.types import SamplingFunction


def stripes(repetitions: int, sampling_function: SamplingFunction, step_ratio: float = 0.1) -> StitchEffect:
    return lambda path: stripes_along(path, repetitions=repetitions, sampling_function=sampling_function,
                                      step_ratio=step_ratio)
