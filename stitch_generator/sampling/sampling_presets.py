from stitch_generator.functions.functions_1d import linear_interpolation, arc
from stitch_generator.sampling.sample_by_density import sampling_by_density
from stitch_generator.sampling.sample_by_fixed_length import sampling_by_fixed_length
from stitch_generator.sampling.sample_by_length import sampling_by_length
from stitch_generator.sampling.sample_by_number import sample_by_number, sampling_by_number
from stitch_generator.sampling.sampling_modifiers import alternate_direction
from stitch_generator.sampling.tatami_sampling import alternating_tatami_sampling


def sampling_presets_stateless(include_endpoint: bool):
    """
    Returns sampling functions which have no internal state, i.e. which always return the same value for the same
    parameter total_length

    Args:
        include_endpoint: True if the sampling functions shall include the endpoint, otherwise False
    """
    yield sampling_by_length(segment_length=3, include_endpoint=include_endpoint)
    yield sampling_by_fixed_length(segment_length=2, include_endpoint=True, alignment=0, offset=0,
                                   minimal_segment_size=0)
    yield sampling_by_fixed_length(segment_length=3, include_endpoint=True, alignment=1, offset=0.5,
                                   minimal_segment_size=0.5)
    yield sampling_by_fixed_length(segment_length=10, include_endpoint=False, alignment=0.5, offset=0,
                                   minimal_segment_size=0.5)
    yield sampling_by_number(number_of_segments=3, include_endpoint=include_endpoint)
    yield sampling_by_density(segment_length=0.5, density_distribution=arc, include_endpoint=include_endpoint)


def sampling_presets(include_endpoint: bool, alignment: float):
    """
    Returns sampling functions which may have an internal state, i.e. the sampling functions may return different
    samples when called again with the same parameter total_length

    Args:
        include_endpoint: True if the sampling functions shall include the endpoint, otherwise False
        alignment: Relative value between 0 and 1 that defines the anchor point relative to which the sampling is done
    """

    yield alternate_direction(sampling_by_fixed_length(segment_length=3, include_endpoint=True,
                                                       alignment=alignment, minimal_segment_size=0.15),
                              include_endpoint=include_endpoint)

    yield alternating_tatami_sampling(stitch_length=4, include_endpoint=True, offsets=(0, 1 / 3, 2 / 3),
                                      alignment=alignment, minimal_segment_size=0.25)

    yield alternating_tatami_sampling(stitch_length=4, include_endpoint=include_endpoint, offsets=[.0] * 10 + [.5] * 10,
                                      alignment=alignment, minimal_segment_size=0.25)

    yield alternating_tatami_sampling(stitch_length=3, include_endpoint=include_endpoint,
                                      offsets=arc(sample_by_number(30, include_endpoint=False)) * 0.5,
                                      alignment=alignment, minimal_segment_size=0.1)

    yield alternating_tatami_sampling(stitch_length=3, include_endpoint=include_endpoint,
                                      offsets=linear_interpolation(0, 0.7)(
                                          sample_by_number(10, include_endpoint=False)),
                                      alignment=alignment, minimal_segment_size=0.1)
