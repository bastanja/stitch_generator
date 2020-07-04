from stitch_generator.design_utilities.embroidery_design import EmbroideryDesign
from stitch_generator.design_utilities.parameter import FloatParameter, IntParameter
from stitch_generator.functions.embroidery_pattern import EmbroideryPattern
from stitch_generator.functions.function_modifiers import combine, add, multiply, repeat, scale, shift
from stitch_generator.functions.functions_1d import noise
from stitch_generator.functions.functions_2d import spiral, circle
from stitch_generator.functions.linspace import samples
from stitch_generator.functions.sample import arc_length_mapping_with_length


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, parameters={
            'stitch_length': FloatParameter("Stitch length", 1, 3, 6),
            'turns': IntParameter("Number of Turns", 1, 10, 15),
            'inner_radius': FloatParameter("Inner radius", 0, 5, 100),
            'outer_radius': FloatParameter("Outer radius", 0, 80, 100),
            'noise_length': FloatParameter("Noise length", 10, 120, 200),
            'noise_offset': FloatParameter("Noise offset", 0, 25, 50),
            'noise_width': FloatParameter("Noise width", 0, 8, 30),
        })

    def get_pattern(self, parameters):
        parameters = self.validate(parameters)
        f = spiral(parameters.inner_radius, parameters.outer_radius, parameters.turns)
        direction = repeat(parameters.turns, circle())

        mapping, length = arc_length_mapping_with_length(f)
        f = combine(mapping, f)
        direction = combine(mapping, direction)

        noise_repetitions = length / parameters.noise_length

        offset = scale(parameters.noise_width,
                       shift(parameters.noise_offset / parameters.noise_length,
                             repeat(noise_repetitions, noise())))

        f = add(f, multiply(direction, offset))

        p = samples(int(round(length / parameters.stitch_length)))

        stitches = f(p)

        pattern = EmbroideryPattern()
        pattern.add_stitches(stitches)

        return pattern