from stitch_generator.framework.path import Path
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.sampling.sample_by_length import sample_by_length
from stitch_generator.utilities.types import Function2D


def running_stitch_along(path: Path, stitch_length: float, include_endpoint: bool = True):
    return path.shape(
        sample_by_length(total_length=path.length, segment_length=stitch_length, include_endpoint=include_endpoint))


def running_stitch_shape(shape: Function2D, stitch_length: float, include_endpoint: bool = True):
    return shape(sample_by_length(total_length=estimate_length(shape), segment_length=stitch_length,
                            include_endpoint=include_endpoint))
