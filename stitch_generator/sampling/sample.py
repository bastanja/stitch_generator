import numpy as np

from stitch_generator.sampling.sample_by_number import sample_by_number


def sample(total_length: float,
           segment_length: float,
           alignment: float,
           include_endpoint: bool,
           offset: float,
           minimal_segment_size: float = 0.5):
    if np.isclose(total_length, 0) or np.isclose(segment_length, 0) or segment_length > total_length:
        return _default_samples(include_endpoint=include_endpoint)

    relative_segment_length = segment_length / total_length
    minimal_segment_length = relative_segment_length * minimal_segment_size

    segment_offset = relative_segment_length * offset
    reference_stitch = (alignment + segment_offset) - minimal_segment_length
    relative_segment_offset = reference_stitch % relative_segment_length + minimal_segment_length

    available_length = 1 - (relative_segment_offset + minimal_segment_length)

    if available_length > 0:
        number_of_segments = int(available_length / relative_segment_length)

        result = [relative_segment_offset + (i * relative_segment_length) for i in range(number_of_segments + 1)]
        if result[0] > 0:
            result.insert(0, 0.0)
        if np.isclose(result[-1], 1.0) and not include_endpoint:
            result.pop(-1)
        if result[-1] < 1 and include_endpoint:
            result.append(1.0)

        return np.array(result)

    return _default_samples(include_endpoint=include_endpoint)


def _default_samples(include_endpoint: bool):
    return sample_by_number(1, include_endpoint=include_endpoint)
