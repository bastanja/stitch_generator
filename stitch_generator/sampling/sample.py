import numpy as np

from stitch_generator.sampling.sample_by_number import sample_by_number


def sample(total_length: float,
           segment_length: float,
           alignment: float,
           offset: float,
           minimal_segment_size: float = 0.5):
    if np.isclose(total_length, 0):
        return _default_samples()

    if segment_length > total_length or np.isclose(segment_length, 0):
        return _default_samples()

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


def _default_samples():
    return sample_by_number(1)
