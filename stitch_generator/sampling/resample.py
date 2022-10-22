import numpy as np
from scipy.interpolate import interp1d

from stitch_generator.framework.types import SamplingFunction
from stitch_generator.functions.estimate_length import accumulate_lengths
from stitch_generator.sampling.sample_by_length import sample_by_length, sampling_by_length
from stitch_generator.shapes.line import line_shape


def polyline(points, smooth: bool = False):
    accumulated = accumulate_lengths(points)
    total_length = accumulated[-1]
    accumulated /= total_length

    kind = 'quadratic' if smooth and len(points) > 2 else 'linear'

    # create interpolation function between points
    interpolation = interp1d(accumulated, points, kind=kind, axis=0)

    return interpolation, total_length


def resample(points, segment_length: float, smooth: bool = False):
    """
    Returns points which lie on the polyline defined by the parameter points. The newly calculated points have
    approximately the distance segment_length.
    """
    return resample_with_sampling_function(points, sampling_function=sampling_by_length(segment_length=segment_length),
                                           smooth=smooth)


def resample_with_sampling_function(points, sampling_function: SamplingFunction, smooth: bool = False):
    """
    Returns points which lie on the polyline defined by the parameter points.
    """
    interpolation, total_length = polyline(points, smooth)

    samples = sampling_function(total_length)
    return interpolation(samples)


def resample_by_segment(points, segment_length):
    result = []
    points = np.asarray(points)
    for p1, p2 in zip(points, points[1:]):
        shape = line_shape(p1, p2)
        samples = sample_by_length(np.linalg.norm(p2 - p1), segment_length)[:-1]
        result.append(shape(samples))
    result.append([points[-1]])
    return np.concatenate(result)
