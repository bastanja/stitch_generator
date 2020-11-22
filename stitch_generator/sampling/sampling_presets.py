from stitch_generator.functions.functions_1d import linear_interpolation, arc
from stitch_generator.sampling.sample_by_fixed_length import sampling_by_fixed_length
from stitch_generator.sampling.sample_by_length import sampling_by_length
from stitch_generator.sampling.sample_by_number import sample_by_number, sampling_by_number
from stitch_generator.sampling.sampling_modifiers import alternate_direction
from stitch_generator.sampling.tatami_sampling import alternating_tatami_sampling


def sampling_presets(include_endpoint: bool, alignment: float):
    yield sampling_by_length(segment_length=3, include_endpoint=include_endpoint)

    yield sampling_by_number(number_of_segments=3, include_endpoint=include_endpoint)

    yield alternate_direction(sampling_by_fixed_length(segment_length=3, include_endpoint=True,
                                                       alignment=alignment, minimal_segment_size=0.15),
                              include_endpoint=include_endpoint)

    yield alternating_tatami_sampling(stitch_length=4, include_endpoint=True, offsets=(0, 1 / 3, 2 / 3),
                                      alignment=alignment, minimal_segment_size=0.25)

    yield alternating_tatami_sampling(stitch_length=4, include_endpoint=include_endpoint, offsets=[.0] * 10 + [.5] * 10,
                                      alignment=alignment, minimal_segment_size=0.25)

    yield alternating_tatami_sampling(stitch_length=3, include_endpoint=include_endpoint,
                                      offsets=arc()(sample_by_number(30, include_endpoint=False)) * 0.5,
                                      alignment=alignment, minimal_segment_size=0.1)

    yield alternating_tatami_sampling(stitch_length=3, include_endpoint=include_endpoint,
                                      offsets=linear_interpolation(0, 0.7)(
                                          sample_by_number(10, include_endpoint=False)),
                                      alignment=alignment, minimal_segment_size=0.1)
