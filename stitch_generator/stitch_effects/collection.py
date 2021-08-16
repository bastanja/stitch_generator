from stitch_generator.functions.connect_functions import line_with_sampling_function, combine_start_end, \
    running_stitch_line
from stitch_generator.functions.function_modifiers import subtract, add, scale, repeat
from stitch_generator.functions.functions_1d import smoothstep, constant, linear_interpolation, cosinus, arc
from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.sampling.sample_by_number import sample_by_number
from stitch_generator.sampling.sampling_modifiers import add_start, add_end
from stitch_generator.sampling.tatami_sampling import tatami_sampling
from stitch_generator.stitch_effects.contour import contour
from stitch_generator.stitch_effects.double_satin import double_satin
from stitch_generator.stitch_effects.lattice import lattice
from stitch_generator.stitch_effects.meander import meander
from stitch_generator.stitch_effects.scribble import scribble
from stitch_generator.stitch_effects.stripes import stripes
from stitch_generator.stitch_effects.underlay_contour_zigzag import underlay_contour_zigzag
from stitch_generator.stitch_effects.underlay_dense import underlay_dense

_cosine_pattern = add(constant(0.5), scale(0.5, repeat(0.5, cosinus)))
_linear_pattern = linear_interpolation(0, 1)
_peaks = subtract(constant(1), repeat(0.5, arc))


def get_tatami(segment_length: float = 3):
    return tatami_sampling(segment_length=segment_length, offsets=sample_by_number(3)[:-1], alignment=0.5,
                           minimal_segment_size=0.5)


def stitch_effects(stitch_length: float):
    yield contour(stitch_length=stitch_length)

    yield double_satin(regular(7), running_stitch_line(stitch_length, False))

    yield lattice(strands=3, pattern_f=_cosine_pattern, pattern_length=10)

    yield lattice(strands=7, pattern_f=_linear_pattern, pattern_length=20)

    yield lattice(strands=3, pattern_f=_linear_pattern, pattern_length=3)

    yield lattice(strands=5, pattern_f=_peaks, pattern_length=25)

    yield lattice(strands=5, pattern_f=smoothstep, pattern_length=25)

    yield meander(sampling_function=regular(1), connect_function=combine_start_end(
        line_with_sampling_function(add_start(add_end(get_tatami(segment_length=stitch_length))))))

    yield meander(sampling_function=regular(3), connect_function=running_stitch_line(stitch_length, True))

    yield stripes(repetitions=6, sampling_function=add_start(get_tatami(segment_length=stitch_length)),
                  step_ratio=0.1)

    yield underlay_dense(inset=0, stitch_length=stitch_length, spacing=2)

    yield underlay_contour_zigzag(inset=0, stitch_length=stitch_length, spacing=4)

    yield scribble(repetitions=12, stitch_length=stitch_length)
