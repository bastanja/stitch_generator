import itertools

import numpy as np

from stitch_generator.designs.wave_paths import make_waves
from stitch_generator.framework.embroidery_design import EmbroideryDesign
from stitch_generator.framework.parameter import FloatParameter
from stitch_generator.functions.connect_functions import line_with_sampling_function
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import inverse
from stitch_generator.sampling.sample_by_length import sampling_by_length
from stitch_generator.sampling.sampling_modifiers import remove_start, remove_end


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="waves", parameters={
            'stitch_length': FloatParameter("Stitch length", 1, 3, 6),
            'width': FloatParameter("Width", 30, 120, 240),
            'height': FloatParameter("Height", 30, 120, 240),
            'line_spacing': FloatParameter("Line spacing", 3, 8, 50),
            'amplitude': FloatParameter("Amplitude", 0, 4, 20),
            'wave_length': FloatParameter("Wave length", 10, 70, 100),
            'initial_offset': FloatParameter("Initial offset", -0.5, 0, 0.5),
            'offset_per_line': FloatParameter("Offset per line", -0.5, 0.25, 0.5)
        })

    def _to_pattern(self, parameters, pattern):
        # create the wave lines
        lines = make_waves(width=parameters.width, height=parameters.height,
                           offset_per_line=parameters.offset_per_line, line_spacing=parameters.line_spacing,
                           amplitude=parameters.amplitude, wave_length=parameters.wave_length,
                           initial_offset=parameters.initial_offset)

        # reverse every other line
        reverse = itertools.cycle((False, True))
        lines = [inverse(line) if next(reverse) else line for line in lines]

        # sample all wave lines to get stitch coordinates
        sampling = sampling_by_length(segment_length=parameters.stitch_length)
        stitch_lines = [line(sampling(estimate_length(line))) for line in lines]

        # connect the endpoint of each line with the start point of the next one
        connect_points = [(first[-1], second[0]) for first, second in zip(stitch_lines, stitch_lines[1:])]
        connect = line_with_sampling_function(remove_start(remove_end(sampling)))
        fills = [connect(p1, p2) for p1, p2 in connect_points]

        # combine stitch lines of the waves and the connection lines
        parts = itertools.zip_longest(stitch_lines, fills)
        combined = [i for i in itertools.chain.from_iterable(parts) if i is not None]

        # add the combined line to the embroidery pattern
        stitches = np.concatenate(combined)
        pattern.add_stitches(stitches)


if __name__ == "__main__":
    Design().cli()
