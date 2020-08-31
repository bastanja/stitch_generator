from functools import partial

from stitch_generator.designs import lattice
from stitch_generator.functions.connect_functions import line_with_sampling_function, combine_start_end
from stitch_generator.functions.samples import samples_by_length, samples, alternate_and_cycle_offset
from stitch_generator.stitch_effects.meander import meander_along

running_stitch_line = line_with_sampling_function(
    sampling_function=partial(samples_by_length, segment_length=3, include_endpoint=True))

sampling_function = partial(samples, segment_length=4, alignment=0.5, minimal_segment_size=0.25)
sampling_function_tatami = alternate_and_cycle_offset(sampling_function=sampling_function, include_endpoint=True,
                                                      offsets=(0, 0.25, 0.5, 0.75))

connect_with_pattern = combine_start_end(line_with_sampling_function(sampling_function_tatami))

stitch_effects = [
    lattice.presets[0],
    partial(meander_along, stitch_spacing=1, connect_function=connect_with_pattern, length=100),
    partial(meander_along, stitch_spacing=3, connect_function=running_stitch_line, length=100),
    lattice.presets[1]
]
