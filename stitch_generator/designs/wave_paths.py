from functools import partial

from stitch_generator.framework.embroidery_design import EmbroideryDesign
from stitch_generator.framework.parameter import FloatParameter
from stitch_generator.framework.path import path_from_boundaries
from stitch_generator.functions.function_modifiers import shift, repeat, combine, add
from stitch_generator.functions.functions_1d import constant, cosinus, linear_interpolation
from stitch_generator.functions.functions_2d import function_2d, constant_direction
from stitch_generator.sampling.sample_by_fixed_length import sampling_by_fixed_length
from stitch_generator.sampling.sampling_modifiers import free_start, free_end
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.path_effects.meander import simple_meander


def make_wave_y(constant_y_offset, amplitude, shift_amount, repetitions):
    f = cosinus
    f = shift(shift_amount, f)
    f = repeat(r=repetitions, function=f, mode='wrap')
    f = combine(f, linear_interpolation(-amplitude, amplitude, source_low=-1, source_high=1))
    f = add(constant(constant_y_offset), f)
    return f


def make_wave(t: float, width: float, height: float, amplitude: float, wave_repeat_x: float,
              wave_repeat_y: float, initial_offset: float):
    half_width = width / 2
    half_height = height / 2
    x_positions = linear_interpolation(-half_width, half_width)
    y_positions = linear_interpolation(-half_height, half_height)

    interpolation_range = 0 if wave_repeat_y == 0 else height / wave_repeat_y
    start = initial_offset - interpolation_range / 2
    end = initial_offset + interpolation_range / 2
    offset_f = linear_interpolation(start, end)

    repetitions = width / wave_repeat_x
    return function_2d(x_positions, make_wave_y(y_positions(t), amplitude, offset_f(t), repetitions))


def make_waves(width: float, height: float, offset_per_line: float, line_spacing: float, amplitude: float,
               wave_length: float, initial_offset: float):
    full_offset_height = 1 / offset_per_line if offset_per_line != 0 else 0
    make_wave_t = partial(make_wave, width=width, height=height,
                          amplitude=amplitude, wave_repeat_x=wave_length,
                          wave_repeat_y=full_offset_height * line_spacing, initial_offset=initial_offset)

    start_end_spacing = amplitude
    line_sampling = sampling_by_fixed_length(line_spacing, alignment=0.5, offset=0.5)
    line_sampling = free_start(start_end_spacing, free_end(start_end_spacing, line_sampling))

    lines = [make_wave_t(t) for t in line_sampling(height)]

    return lines


def make_wave_paths(width: float, height: float, gap_size: float, lines):
    half_width = width / 2
    half_height = height / 2
    half_gap = gap_size / 2

    first_line = line(origin=(-half_width, -half_height), to=(half_width, -half_height))
    last_line = line(origin=(-half_width, half_height), to=(half_width, half_height))

    left_boundaries = [add(constant_direction(0, -half_gap), f) for f in lines] + [last_line]
    right_boundaries = [first_line] + [add(constant_direction(0, half_gap), f) for f in lines]

    return [path_from_boundaries(left, right) for left, right in zip(left_boundaries, right_boundaries)]


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="wave_paths", parameters={
            'stitch_length': FloatParameter("Stitch length", 1, 3, 6),
            'meander_spacing': FloatParameter("Meander Spacing", 1, 3, 6),
            'width': FloatParameter("Width", 10, 100, 200),
            'height': FloatParameter("Height", 10, 100, 200),
            'line_spacing': FloatParameter("Line spacing", 5, 12, 50),
            'amplitude': FloatParameter("Amplitude", 0, 3, 12),
            'wave_length': FloatParameter("Wave length", 10, 50, 100),
            'initial_offset': FloatParameter("Initial offset", 0, 0.25, 1),
            'offset_per_line': FloatParameter("Offset per line", -1, 0.5, 1),
            'gap': FloatParameter("Gap", 0, 2, 5)
        })

    def _to_pattern(self, parameters, pattern):
        lines = make_waves(width=parameters.width, height=parameters.height - (2 * parameters.gap),
                           offset_per_line=parameters.offset_per_line, line_spacing=parameters.line_spacing,
                           amplitude=parameters.amplitude, wave_length=parameters.wave_length,
                           initial_offset=parameters.initial_offset)

        paths = make_wave_paths(width=parameters.width, height=parameters.height, gap_size=parameters.gap, lines=lines)

        effect = simple_meander(spacing=parameters.meander_spacing, stitch_length=parameters.stitch_length)

        for path in paths:
            path.length = parameters.width
            pattern.add_stitches(effect(path))

        if __name__ == "__main__":
            Design().cli()
