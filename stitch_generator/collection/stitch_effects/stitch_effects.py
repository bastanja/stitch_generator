from stitch_generator.collection.functions.functions_1d import half_cosine_positive, linear_0_1, half_peak
from stitch_generator.collection.sampling.tatami_sampling import tatami_3_1
from stitch_generator.collection.stitch_effects.underlay_contour_zigzag import underlay_contour_zigzag
from stitch_generator.collection.stitch_effects.underlay_dense import underlay_dense
from stitch_generator.functions.functions_1d import smoothstep
from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.sampling.sample_by_number import sample_by_number
from stitch_generator.sampling.sampling_modifiers import add_start, add_end, alternate_direction, remove_end
from stitch_generator.stitch_effects.path_effects.contour import contour
from stitch_generator.stitch_effects.path_effects.double_satin import double_satin
from stitch_generator.stitch_effects.path_effects.lattice import lattice
from stitch_generator.stitch_effects.path_effects.meander import meander
from stitch_generator.stitch_effects.path_effects.scribble import scribble
from stitch_generator.stitch_effects.path_effects.stripes import stripes, parallel_stripes


def stitch_effects(stitch_length: float):
    yield contour(stitch_length=stitch_length)

    yield double_satin(spacing_function=regular(7), line_sampling_function=remove_end(regular(stitch_length)))

    yield lattice(strands=3, pattern_f=half_cosine_positive, pattern_length=10)

    yield lattice(strands=7, pattern_f=linear_0_1, pattern_length=20)

    yield lattice(strands=3, pattern_f=linear_0_1, pattern_length=3)

    yield lattice(strands=5, pattern_f=half_peak, pattern_length=25)

    yield lattice(strands=5, pattern_f=smoothstep, pattern_length=25)

    yield meander(spacing_function=regular(1), line_sampling_function=add_start(
        add_end(alternate_direction(tatami_3_1(segment_length=stitch_length)))), join_ends=True)

    yield meander(spacing_function=regular(3), line_sampling_function=regular(segment_length=stitch_length))

    yield stripes(repetitions=6,
                  sampling_function=add_start(alternate_direction(tatami_3_1(segment_length=stitch_length))),
                  step_ratio=0.1)

    yield parallel_stripes(steps=sample_by_number(6),
                           sampling_function=add_start(add_end(tatami_3_1(segment_length=stitch_length))))

    yield underlay_dense(inset=0, stitch_length=stitch_length, spacing=2)

    yield underlay_contour_zigzag(inset=0, stitch_length=stitch_length, spacing=4)

    yield scribble(repetitions=12, sampling_function=add_start(alternate_direction(tatami_3_1(stitch_length))),
                   noise_offset=1.5)