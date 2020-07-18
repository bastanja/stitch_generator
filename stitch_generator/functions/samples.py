import numpy as np


def samples_by_segments(number_of_segments: int, include_endpoint: bool):
    return linspace(start=0, stop=1, number_of_segments=number_of_segments, include_endpoint=include_endpoint)


def samples_by_length(total_length: float, segment_length: float, include_endpoint: bool):
    assert segment_length > 0, "segment_length must be > 0"
    number_of_segments = int(round(total_length / segment_length))
    number_of_segments = max(1, number_of_segments)
    return linspace(start=0, stop=1, number_of_segments=number_of_segments, include_endpoint=include_endpoint)


def samples_by_fixed_length(total_length: float, segment_length: float):
    assert segment_length > 0, "segment_length must be > 0"
    number_of_segments = int(total_length / segment_length)
    if total_length > 0:
        segment_length = segment_length / total_length
    segment_borders = [i * segment_length for i in range(number_of_segments + 1)]
    return np.array(segment_borders)


def samples_by_fixed_length_with_offset(total_length: float, segment_length: float, offset: float):
    assert segment_length > 0, "segment_length must be > 0"
    start_segment_length = segment_length * offset
    number_of_segments = int((total_length - start_segment_length) / segment_length)
    if total_length > 0:
        segment_length = segment_length / total_length
    segment_borders = [i * segment_length for i in range(number_of_segments + 1)]
    return np.array(segment_borders)


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
