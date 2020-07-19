import numpy as np


def samples_by_segments(number_of_segments: int, include_endpoint: bool):
    return linspace(start=0, stop=1, number_of_segments=number_of_segments, include_endpoint=include_endpoint)


def samples_by_length(total_length: float, segment_length: float, include_endpoint: bool):
    if np.isclose(total_length, 0) or np.isclose(segment_length, 0) or segment_length > total_length:
        return _default_samples(include_endpoint=include_endpoint)

    number_of_segments = int(round(total_length / segment_length))
    return linspace(start=0, stop=1, number_of_segments=number_of_segments, include_endpoint=include_endpoint)


def samples_by_fixed_length(total_length: float, segment_length: float):
    if np.isclose(total_length, 0) or np.isclose(segment_length, 0) or segment_length > total_length:
        return _default_samples(include_endpoint=False)

    number_of_segments = int(total_length / segment_length)
    segment_length = segment_length / total_length
    segment_borders = [i * segment_length for i in range(number_of_segments + 1)]
    return np.array(segment_borders)


def samples_by_fixed_length_with_alignment(total_length: float,
                                           segment_length: float,
                                           alignment: float,
                                           minimal_segment_size: float = 0.5):
    if np.isclose(total_length, 0) or np.isclose(segment_length, 0) or segment_length > total_length:
        return _default_samples(include_endpoint=True)

    relative_segment_length = segment_length / total_length
    minimal_segment_length = relative_segment_length * minimal_segment_size
    relative_segment_offset = (alignment - minimal_segment_length) % relative_segment_length + minimal_segment_length

    available_length = 1 - (relative_segment_offset + minimal_segment_length)
    if available_length > 0:
        number_of_segments = int(available_length / relative_segment_length)

        result = np.zeros(number_of_segments + 3, dtype=float)
        result[-1] = 1
        result[1:-1] = [relative_segment_offset + (i * relative_segment_length) for i in range(number_of_segments + 1)]
        return result
    return _default_samples(include_endpoint=True)


def mid_samples_by_segments(number_of_segments: int):
    return linspace_mid(start=0, stop=1, number_of_segments=number_of_segments)


def linspace(start: float, stop: float, number_of_segments: int, include_endpoint: bool):
    number_of_samples = number_of_segments + 1 if include_endpoint else number_of_segments
    return np.linspace(start, stop, num=number_of_samples, endpoint=include_endpoint)


def linspace_mid(start: float, stop: float, number_of_segments):
    l = linspace(start, stop, number_of_segments, include_endpoint=True)
    offset = (l[1] - l[0]) / 2
    l += offset
    return l[0:-1]


def _default_samples(include_endpoint: bool):
    return linspace(0, 1, 1, include_endpoint=include_endpoint)
