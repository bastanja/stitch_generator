from stitch_generator.designs import lattice
from stitch_generator.functions.connect_functions import line_with_sampling_function, combine_start_end, \
    running_stitch_line
from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.sampling.tatami_sampling import alternating_tatami_sampling
from stitch_generator.stitch_effects.contour import contour
from stitch_generator.stitch_effects.double_satin import double_satin
from stitch_generator.stitch_effects.meander import meander
from stitch_generator.stitch_effects.stripes import stripes
from stitch_generator.stitch_effects.underlay_contour_zigzag import underlay_contour_zigzag
from stitch_generator.stitch_effects.underlay_dense import underlay_dense


def get_tatami(include_endpoint=True, stitch_length: float = 3):
    return alternating_tatami_sampling(stitch_length=stitch_length, include_endpoint=include_endpoint,
                                       offsets=(0, 1 / 3, 2 / 3), alignment=0.5, minimal_segment_size=0.5)


def stitch_effects(stitch_length: float):
    yield contour(stitch_length=stitch_length)

    yield double_satin(regular(7), running_stitch_line(stitch_length, False))

    yield lattice.presets[0]

    yield lattice.presets[1]

    yield meander(sampling_function=regular(1), connect_function=combine_start_end(
        line_with_sampling_function(get_tatami(include_endpoint=True, stitch_length=stitch_length))))

    yield meander(sampling_function=regular(3), connect_function=running_stitch_line(stitch_length, True))

    yield stripes(repetitions=6,
                        sampling_function=get_tatami(include_endpoint=False, stitch_length=stitch_length),
                        step_ratio=0.1)

    yield underlay_dense(inset=0, stitch_length=stitch_length, spacing=2)

    yield underlay_contour_zigzag(inset=0, stitch_length=stitch_length, spacing=4)
