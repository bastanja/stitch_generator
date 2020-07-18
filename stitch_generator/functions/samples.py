import numpy as np


def samples_by_segments(number_of_segments: int, include_endpoint: bool):
    return linspace(start=0, stop=1, number_of_segments=number_of_segments, include_endpoint=include_endpoint)


def mid_samples_by_segments(number_of_segments: int):
    return linspace_mid(start=0, stop=1, number_of_segments=number_of_segments)


def linspace(start: float, stop: float, number_of_segments: int, include_endpoint: bool):
    number_of_samples = number_of_segments + 1 if include_endpoint else number_of_segments
    return np.linspace(start, stop, num=number_of_samples, endpoint=include_endpoint)


def divide_equally(start: float, stop: float, segment_length, include_endpoint: bool):
    assert segment_length > 0, "segment_length must be > 0"
    num_segments = int(round((stop - start) / segment_length))
    num_segments = max(1, num_segments)
    return linspace(start, stop, num_segments, include_endpoint)


def divide_exact(start: float, stop: float, segment_length):
    number_of_segments = int((stop - start) / segment_length)
    segment_borders = [start + i * segment_length for i in range(number_of_segments + 1)]
    return np.array(segment_borders)


def linspace_mid(start: float, stop: float, number_of_segments):
    l = linspace(start, stop, number_of_segments, include_endpoint=True)
    offset = (l[1] - l[0]) / 2
    l += offset
    return l[0:-1]
