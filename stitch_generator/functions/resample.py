from scipy.interpolate import interp1d

from stitch_generator.functions.estimate_length import accumulate_lengths
from stitch_generator.sampling.sampling import regular_sampling


def resample(stitches, stitch_length):
    """
    Returns stitches which lie the polyline defined by the parameter stitches. The newly calculated stitches have
    approximately the distance stitch_length. This function can be used to increase or decrease the stitch density.
    """
    accumulated = accumulate_lengths(stitches)
    total_length = accumulated[-1]
    accumulated /= total_length

    # create interpolation function between stitches
    interpolation = interp1d(accumulated, stitches, kind='linear', axis=0)

    samples = regular_sampling(stitch_length=stitch_length, include_endpoint=True)(total_length)
    return interpolation(samples)
