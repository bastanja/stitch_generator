import numpy as np

from stitch_generator.collection.sampling_with_offset_function import triangle_sampling, sampling_with_offset_function, \
    arc_sampling, wave_sampling
from stitch_generator.collection.tatami_sampling import tatami_3_1, tatami_4_2
from stitch_generator.framework.embroidery_design import EmbroideryDesign
from stitch_generator.framework.palette import palette
from stitch_generator.framework.parameter import FloatParameter, BoolParameter
from stitch_generator.framework.path import Path
from stitch_generator.functions.arc_length_mapping import arc_length_mapping_with_length
from stitch_generator.functions.connect_functions import combine_start_end, line_with_sampling_function
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import combine, add
from stitch_generator.functions.function_sequence import function_sequence
from stitch_generator.functions.functions_1d import constant, circular_arc, linear_interpolation, pchip_interpolation, \
    arc, sinus
from stitch_generator.functions.functions_2d import constant_direction
from stitch_generator.sampling.sample_by_length import sampling_by_length
from stitch_generator.sampling.sampling_modifiers import add_start, add_end, alternate_direction, free_start, free_end
from stitch_generator.shapes.bezier import bezier_normals, bezier
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.meander import meander
from stitch_generator.stitch_effects.underlay_contour_zigzag import underlay_contour_zigzag
from stitch_generator.stitch_effects.underlay_dense import underlay_dense


def make_shape_linear():
    shape = line(origin=(-25, 0), to=(25, 0))
    direction = constant_direction(0, -1)
    return shape, direction


def make_shape():
    points = (3, 25), (-14, -1), (11, -5), (-2, -25)
    shape = bezier(points)
    mapping, length = arc_length_mapping_with_length(shape)
    shape = combine(mapping, shape)
    direction = combine(mapping, bezier_normals(points))

    return shape, direction


def make_width(width, length):
    width_profile = pchip_interpolation(((0, 1), (0.68, 0.68), (1, 0)))
    radius = width / 2
    width_f = function_sequence((circular_arc, width_profile), (radius, length - radius))
    width_f = combine(width_f, linear_interpolation(0.5, width))
    alignment = constant(0.5)
    return width_f, alignment


def make_paths(offsets, max_width, shape_function):
    shape, direction = shape_function()
    width, alignment = make_width(max_width, estimate_length(shape))
    paths = [Path(add(constant_direction(x, y), shape), direction, width, alignment) for x, y in offsets]
    return paths


def free_start_end(sampling_function):
    return free_start(1, free_end(1, sampling_function))


def sampling_functions():
    yield tatami_3_1(segment_length=4)
    yield tatami_4_2(segment_length=3)
    yield free_start_end(alternate_direction(triangle_sampling(segment_length=3.5, steps=30)))
    yield free_start_end(arc_sampling(segment_length=3, steps=30, function_range=(0.75, 0.25)))
    yield free_start_end(wave_sampling(segment_length=3, steps=60, function_range=(0.2, 0.8)))
    yield free_start_end(triangle_sampling(segment_length=3, steps=40))


def make_stitch_effects(satin_spacing):
    connect_functions = [combine_start_end(line_with_sampling_function(add_start(add_end(alternate_direction(f)))))
                         for f in sampling_functions()]

    effects = [meander(sampling_function=sampling_by_length(satin_spacing), connect_function=f) for f in
               connect_functions]

    return effects


def get_underlay(dense: bool, inset: float, spacing: float):
    stitch_length = 2.5
    if dense:
        return underlay_dense(inset=inset, stitch_length=stitch_length, spacing=spacing)
    return underlay_contour_zigzag(inset=inset, stitch_length=stitch_length, spacing=spacing)


def get_offsets(distance, lines):
    half_width = (lines - 1) * distance / 2
    return [(x, 0) for x in [(distance * i) - half_width for i in range(lines)]]


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="satin_samples", parameters={
            'width': FloatParameter("Line Width", 4, 8, 12),
            'satin_spacing': FloatParameter("satin spacing", 0.1, 0.2, 0.4),
            'distance_x': FloatParameter("Distance X", 10, 11, 25),
            'hide_underlay': BoolParameter("Hide underlay", False),
            'dense_underlay': BoolParameter("Dense underlay", True),
            'underlay_inset': FloatParameter("Underlay inset", 0, 0.5, 2),
            'underlay_spacing': FloatParameter("Underlay spacing", 0.5, 1.5, 5),
        })

    def _to_pattern(self, parameters, pattern):
        color = palette()

        stitch_effects = make_stitch_effects(parameters.satin_spacing)

        offsets = get_offsets(parameters.distance_x, len(stitch_effects))

        paths = make_paths(offsets, parameters.width, make_shape)

        underlay = get_underlay(parameters.dense_underlay, parameters.underlay_inset, parameters.underlay_spacing)

        for path, stitch_effect in zip(paths, stitch_effects):
            stitches = stitch_effect(path)
            if not parameters.hide_underlay:
                underlay_stitches = underlay(path)
                stitches = np.concatenate((underlay_stitches, stitches))
            pattern.add_stitches(stitches, next(color))


if __name__ == "__main__":
    Design().cli()
