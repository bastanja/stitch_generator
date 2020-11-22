from scipy.interpolate import interp1d

from stitch_generator.functions.estimate_length import accumulate_lengths
from stitch_generator.utilities.types import SamplingFunction
from stitch_generator.sampling.sample_by_length import sample_by_length


def resample(stitches, stitch_length):
    """
    Returns stitches which lie the polyline defined by the parameter stitches. The newly calculated stitches have
    approximately the distance stitch_length. This function can be used to increase or decrease the stitch density.
    """
    interpolation, total_length = _get_interpolation_and_length(stitches)

    samples = sample_by_length(total_length=total_length, segment_length=stitch_length, include_endpoint=True)
    return interpolation(samples)


def resample_with_sampling_function(stitches, sampling_function: SamplingFunction):
    """
    Returns stitches which lie the polyline defined by the parameter stitches.
    """
    interpolation, total_length = _get_interpolation_and_length(stitches)

    samples = sampling_function(total_length)
    return interpolation(samples)


def _get_interpolation_and_length(stitches):
    accumulated = accumulate_lengths(stitches)
    total_length = accumulated[-1]
    accumulated /= total_length

    # create interpolation function between stitches
    interpolation = interp1d(accumulated, stitches, kind='linear', axis=0)

    return interpolation, total_length
