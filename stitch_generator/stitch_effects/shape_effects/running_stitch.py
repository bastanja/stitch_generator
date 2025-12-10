from stitch_generator.framework import StitchEffect, CoordinateFunction, Coordinates
from stitch_generator.functions import estimate_length
from stitch_generator.subdivision import remove_end
from stitch_generator.subdivision import subdivision_by_length


def running_stitch(stitch_length: float, include_endpoint: bool = True) -> StitchEffect:
    """Creates a running stitch effect along the shape of the path.

    A simple running stitch that follows the shape of the path. The stitches are evenly spaced
    along the path based on the specified stitch length.

    Args:
        stitch_length: The length of each stitch segment along the path.
        include_endpoint: Whether to include the endpoint of the path. Defaults to True.

    Returns:
        A StitchEffect function that takes a Path and returns Coordinates.

    Example:
        ```python
        from stitch_generator.stitch_effects.running_stitch import running_stitch

        effect = running_stitch(stitch_length=3)
        stitches = effect(path)
        ```
    """
    return lambda path: running_stitch_on_shape(
        shape=path.shape, stitch_length=stitch_length, include_endpoint=include_endpoint
    )


def running_stitch_on_shape(
    shape: CoordinateFunction, stitch_length: float, include_endpoint: bool = True
) -> Coordinates:
    """Creates a running stitch directly on a shape function.
    This is the low-level function that works directly with shape functions, without requiring a
    full Path object.

    Args:
        shape: A CoordinateFunction that defines the center line of the path.
        stitch_length: The length of each stitch segment along the path.
        include_endpoint: Whether to include the endpoint of the path. Defaults to True.

    Returns:
        An array of stitch coordinates.
    """
    total_length = estimate_length(shape)
    subdivision = subdivision_by_length(segment_length=stitch_length)
    if not include_endpoint:
        subdivision = remove_end(subdivision)
    offsets = subdivision(total_length)
    return shape(offsets)
