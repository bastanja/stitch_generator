from functools import partial

from stitch_generator.designs import lattice
from stitch_generator.functions.connect_functions import line_with_sampling_function, combine_start_end, \
    running_stitch_line
from stitch_generator.functions.sampling import alternating_tatami_sampling
from stitch_generator.stitch_effects.meander import meander_along


def stitch_effects():
    yield lattice.presets[0]
    yield partial(meander_along, stitch_spacing=1,
                  connect_function=combine_start_end(
                      line_with_sampling_function(alternating_tatami_sampling(stitch_length=4, include_endpoint=True,
                                                                              offsets=(0, 0.25, 0.5, 0.75),
                                                                              alignment=0.5,
                                                                              minimal_segment_size=0.1))), length=100)
    yield partial(meander_along, stitch_spacing=3, connect_function=running_stitch_line(3, True), length=100)
    yield lattice.presets[1]
