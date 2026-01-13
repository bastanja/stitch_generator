from stitch_generator.framework import StitchEffect
from stitch_generator.framework import Function2D
from stitch_generator.functions import estimate_length
from stitch_generator.subdivision import subdivision_by_length
from stitch_generator.subdivision import remove_end


def running_stitch(stitch_length: float, include_endpoint: bool = True) -> StitchEffect:
    return lambda path: running_stitch_on_shape(
        shape=path.shape, stitch_length=stitch_length, include_endpoint=include_endpoint
    )


def running_stitch_on_shape(
    shape: Function2D, stitch_length: float, include_endpoint: bool = True
):
    total_length = estimate_length(shape)
    subdivision = subdivision_by_length(segment_length=stitch_length)
    if not include_endpoint:
        subdivision = remove_end(subdivision)
    offsets = subdivision(total_length)
    return shape(offsets)
