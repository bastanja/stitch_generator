import numpy as np

from stitch_generator.sampling.sample_by_number import sample_by_number
from stitch_generator.sampling.sampling_modifiers import ensure_start_end


def sample(total_length: float,
           segment_length: float,
           alignment: float,
           include_endpoint: bool,
           offset: float,
           minimal_segment_size: float = 0.5):
    # return only start point if the total length is 0
    if np.isclose(total_length, 0):
        return sample_by_number(1, include_endpoint=False)

    # return start point and optionally end point if the segment length is bigger than the total length
    if segment_length > total_length or np.isclose(segment_length, 0):
        return _default_samples(include_endpoint)

    # get the distributed samples
    result = sample_inner(total_length, segment_length, alignment, offset, minimal_segment_size)

    if len(result) == 0:
        return _default_samples(include_endpoint)

    # add or remove start and end points
    result = ensure_start_end(result, include_startpoint=True, include_endpoint=include_endpoint)

    return result


def sample_inner(total_length: float, segment_length: float, alignment: float, offset: float,
                 minimal_segment_size: float):
    # return only start point if the total length is 0
    if np.isclose(total_length, 0):
        return []
    relative_segment_length = segment_length / total_length
    minimal_segment_length = relative_segment_length * minimal_segment_size

    segment_offset = relative_segment_length * offset
    reference_stitch = (alignment + segment_offset) - minimal_segment_length
    relative_segment_offset = reference_stitch % relative_segment_length + minimal_segment_length

    available_length = 1 - (relative_segment_offset + minimal_segment_length)

    if available_length <= 0:
        return []

    number_of_segments = int(available_length / relative_segment_length)
    result = [relative_segment_offset + (i * relative_segment_length) for i in range(number_of_segments + 1)]

    return np.array(result)


def _default_samples(include_endpoint: bool):
    return sample_by_number(1, include_endpoint=include_endpoint)
