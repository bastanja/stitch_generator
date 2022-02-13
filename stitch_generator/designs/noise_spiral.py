from stitch_generator.framework.embroidery_design import EmbroideryDesign
from stitch_generator.framework.palette import palette
from stitch_generator.framework.parameter import FloatParameter, IntParameter
from stitch_generator.framework.path import Path
from stitch_generator.functions.arc_length_mapping import arc_length_mapping_with_length
from stitch_generator.functions.function_modifiers import combine, add, multiply, repeat, scale, shift
from stitch_generator.functions.functions_1d import constant
from stitch_generator.functions.motif_generators import repeat_motif_mirrored
from stitch_generator.functions.noise import noise
from stitch_generator.motifs.satin_circle import satin_circle
from stitch_generator.sampling.sample_by_length import regular, sampling_by_length
from stitch_generator.sampling.sampling_modifiers import free_start_end, remove_end
from stitch_generator.shapes.circle import circle
from stitch_generator.shapes.spiral import spiral
from stitch_generator.stitch_effects.shape_effects.motif_to_points import motif_to_points


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="noise_spiral", parameters={
            'stitch_length': FloatParameter("Stitch length", 1, 3, 6),
            'turns': IntParameter("Number of Turns", 1, 6, 15),
            'inner_radius': FloatParameter("Inner radius", 0, 5, 100),
            'outer_radius': FloatParameter("Outer radius", 0, 80, 100),
            'noise_length': FloatParameter("Noise length", 10, 165, 300),
            'noise_offset': FloatParameter("Noise offset", 0, 30, 150),
            'noise_width': FloatParameter("Noise width", 0, 14, 30),
            'dot_spacing': FloatParameter("Dot spacing", 5, 50, 100),
            'dot_diameter': FloatParameter("Dot diameter", 2, 4, 12),
            'start_spacing': FloatParameter("Start Spacing", 0, 30, 50),
            'end_spacing': FloatParameter("End Spacing", 0, 0, 50),
        })

    def _to_pattern(self, parameters, pattern):
        color = palette()
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

        path = Path(shape=f, direction=direction, width=constant(1), stroke_alignment=constant(0.5))

        dot = satin_circle(diameter=parameters.dot_diameter, stitch_length=parameters.stitch_length,
                           pull_compensation=0.1 * parameters.dot_diameter, return_to_start=True)
        motif_gen = repeat_motif_mirrored(dot - dot[0])

        sampling = free_start_end(parameters.start_spacing, parameters.end_spacing, regular(parameters.dot_spacing))

        effect = motif_to_points(motif_position_sampling=sampling,
                                 line_sampling=remove_end(sampling_by_length(parameters.stitch_length)),
                                 motif_generator=motif_gen)

        stitches = effect(path)

        pattern.add_stitches(stitches, next(color))


if __name__ == "__main__":
    Design().cli()
