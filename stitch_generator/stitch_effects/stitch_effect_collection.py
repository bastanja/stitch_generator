from functools import partial

from stitch_generator.designs import lattice
from stitch_generator.functions.connect_functions import line_with_sampling_function, combine_start_end, \
    running_stitch_line
from stitch_generator.functions.sampling import alternating_tatami_sampling, regular
from stitch_generator.stitch_effects.meander import meander_along
from stitch_generator.stitch_effects.repeat_along import repeat_along


def get_tatami(include_endpoint=True):
    return alternating_tatami_sampling(stitch_length=4, include_endpoint=include_endpoint, offsets=(0, 1 / 3, 2 / 3),
                                       alignment=0.5, minimal_segment_size=0.5)


def stitch_effects(length: float):
    yield lattice.presets[0]

    yield partial(meander_along, sampling_function=regular(1), connect_function=combine_start_end(
        line_with_sampling_function(get_tatami())), length=length)

    yield partial(meander_along, sampling_function=regular(3), connect_function=running_stitch_line(3, True),
                  length=length)

    yield lattice.presets[1]

    yield partial(repeat_along, repetitions=11, sampling_function=get_tatami(False), length=length, step_ratio=0.1)
