from stitch_generator.framework.path import Path
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.sampling.sample_by_length import sampling_by_length
from stitch_generator.sampling.sampling_modifiers import remove_end
from stitch_generator.framework.types import Function2D


def running_stitch_along(path: Path, stitch_length: float, include_endpoint: bool = True):
    samples = _sampling(stitch_length=stitch_length, include_endpoint=include_endpoint)(path.length)
    return path.shape(samples)


def running_stitch_shape(shape: Function2D, stitch_length: float, include_endpoint: bool = True):
    samples = _sampling(stitch_length=stitch_length, include_endpoint=include_endpoint)(estimate_length(shape))
    return shape(samples)


def _sampling(stitch_length: float, include_endpoint: bool):
    sampling = sampling_by_length(segment_length=stitch_length)
    if not include_endpoint:
        sampling = remove_end(sampling)
    return sampling
