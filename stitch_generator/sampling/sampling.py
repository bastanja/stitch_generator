import itertools
from functools import partial
from typing import Iterable

import numpy as np

from stitch_generator.functions.functions_1d import arc, linear_interpolation
from stitch_generator.sampling.samples import samples, samples_by_length, linspace, samples_by_segments, \
    mid_samples_by_length
from stitch_generator.functions.types import SamplingFunction


def regular(stitch_length: float):
    return partial(samples_by_length, segment_length=stitch_length, include_endpoint=True)


def mid_regular(stitch_length: float):
    return partial(mid_samples_by_length, segment_length=stitch_length)


def regular_sampling(stitch_length: float, include_endpoint: bool):  # -> SamplingFunction
    return partial(samples_by_length, segment_length=stitch_length, include_endpoint=include_endpoint)


def segment_sampling(number_of_segments: int, include_endpoint: bool) -> SamplingFunction:
    def f(total_length: float):  # total_length is ignored
        return samples_by_segments(number_of_segments, include_endpoint)

    return f


def fixed_sampling(stitch_length: float, include_endpoint: bool, alignment: float = 0,
                   minimal_segment_size: float = 0.1):  # -> SamplingFunction
    return partial(samples, segment_length=stitch_length, alignment=alignment, include_endpoint=include_endpoint,
                   offset=0, minimal_segment_size=minimal_segment_size)


def fixed_sampling_with_offset(stitch_length: float, include_endpoint: bool, offset: float,
                               alignment: float = 0, minimal_segment_size: float = 0.1):  # -> SamplingFunction
    return partial(samples, segment_length=stitch_length, alignment=alignment, include_endpoint=include_endpoint,
                   offset=offset, minimal_segment_size=minimal_segment_size)


def tatami_sampling(stitch_length: float, include_endpoint: bool, offsets: Iterable[float], alignment: float,
                    minimal_segment_size: float = 0.25) -> SamplingFunction:
    offset_gen = itertools.cycle(offsets)
    sampling_function = partial(samples, segment_length=stitch_length, alignment=alignment,
                                include_endpoint=include_endpoint, minimal_segment_size=minimal_segment_size)

    def f(total_length: float):
        return sampling_function(offset=next(offset_gen), total_length=total_length)

    return f


def alternating_tatami_sampling(stitch_length: float, include_endpoint: bool, offsets: Iterable[float],
                                alignment: float, minimal_segment_size: float = 0.25) -> SamplingFunction:
    sampling_function = tatami_sampling(stitch_length=stitch_length, offsets=offsets, alignment=alignment,
                                        include_endpoint=True, minimal_segment_size=minimal_segment_size)
    forward = itertools.cycle((True, False))

    def f(total_length: float):
        s = sampling_function(total_length)

        if not next(forward):
            s = np.flip(1 - s, axis=0)

        return s if include_endpoint else s[0:-1]

    return f


def free_start_end(start_length: float, end_length: float, sampling_function: SamplingFunction):
    def f(total_length: float):
        cut_length = start_length + end_length
        if total_length > cut_length:
            start_offset = linear_interpolation(0, 1, 0, total_length)(start_length)
            sampled_part = total_length - cut_length
            scale = sampled_part / total_length
            samples = sampling_function(total_length - cut_length) * scale
            return samples + start_offset
        else:
            return np.array((), ndmin=2)

    return f


def presets(include_endpoint: bool, alignment: float):
    yield regular_sampling(stitch_length=3, include_endpoint=include_endpoint)

    yield segment_sampling(number_of_segments=3, include_endpoint=include_endpoint)

    yield fixed_sampling(stitch_length=3, include_endpoint=include_endpoint, alignment=alignment)

    yield alternating_tatami_sampling(stitch_length=4, include_endpoint=True, offsets=(0, 1 / 3, 2 / 3),
                                      alignment=alignment, minimal_segment_size=0.25)

    yield alternating_tatami_sampling(stitch_length=4, include_endpoint=include_endpoint, offsets=[.0] * 10 + [.5] * 10,
                                      alignment=alignment, minimal_segment_size=0.25)

    yield alternating_tatami_sampling(stitch_length=3, include_endpoint=include_endpoint,
                                      offsets=arc()(linspace(0, 1, 30, include_endpoint=False)) * 0.5,
                                      alignment=alignment, minimal_segment_size=0.1)

    yield alternating_tatami_sampling(stitch_length=3, include_endpoint=include_endpoint,
                                      offsets=linear_interpolation(0, 0.7)(linspace(0, 1, 10, include_endpoint=False)),
                                      alignment=alignment, minimal_segment_size=0.1)
