import itertools
from functools import partial

import numpy as np


def samples_by_segments(number_of_segments: int, include_endpoint: bool):
    return linspace(start=0, stop=1, number_of_segments=number_of_segments, include_endpoint=include_endpoint)


def samples_by_length(total_length: float, segment_length: float, include_endpoint: bool):
    if np.isclose(total_length, 0) or np.isclose(segment_length, 0) or segment_length > total_length:
        return _default_samples(include_endpoint=include_endpoint)

    number_of_segments = int(round(total_length / segment_length))
    return linspace(start=0, stop=1, number_of_segments=number_of_segments, include_endpoint=include_endpoint)


def samples(total_length: float,
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


samples_by_fixed_length_with_alignment = partial(samples, offset=0)

samples_by_fixed_length = partial(samples, offset=0, alignment=0.0,
                                  minimal_segment_size=0.0)


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


def alternate_and_cycle_offset(sampling_function, offsets, include_endpoint: bool):
    forward = itertools.cycle((True, False))
    offset_gen = itertools.cycle(offsets)

    def f(**kwargs):
        s = sampling_function(**kwargs, include_endpoint=True, offset=next(offset_gen))

        if not next(forward):
            s = np.flip(1 - s, axis=0)
        return s if include_endpoint else s[0:-1]

    return f


alternate_direction = partial(alternate_and_cycle_offset, offsets=[0])

def _default_samples(include_endpoint: bool):
    return linspace(0, 1, 1, include_endpoint=include_endpoint)