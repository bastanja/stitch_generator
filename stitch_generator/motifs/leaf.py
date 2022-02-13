from functools import partial

import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.functions.arc_length_mapping import arc_length_mapping
from stitch_generator.functions.connect_functions import simple_connect
from stitch_generator.functions.function_modifiers import combine, split, scale, inverse, repeat
from stitch_generator.functions.functions_1d import constant, arc
from stitch_generator.functions.get_boundaries import get_boundaries
from stitch_generator.functions.get_underlay_path import get_underlay_path
from stitch_generator.sampling.sample_by_length import sample_by_length, sampling_by_length
from stitch_generator.sampling.sample_by_number import sample_by_number
from stitch_generator.sampling.sampling_modifiers import remove_end
from stitch_generator.shapes.bezier import bezier, bezier_normals
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.path_effects.stripes import stripes_along
from stitch_generator.stitch_effects.shape_effects.running_stitch import running_stitch_on_shape
from stitch_generator.stitch_effects.path_effects.satin import satin_along
from stitch_generator.stitch_operations.rotate import rotate_by_degrees
from stitch_generator.framework.types import Function1D


def leaf(stem_length: float, leaf_length: float, leaf_width: float, angle_degrees: float, stitch_length: float,
         contour_repetitions: int = 1):
    return _leaf(stem_length, leaf_length, leaf_width, angle_degrees, stitch_length, contour_repetitions,
                 middle_line_length=0)


def satin_leaf(stem_length: float, leaf_length: float, leaf_width: float, angle_degrees: float, stitch_length: float,
               satin_spacing: float = 0.2, underlay_inset: float = 0.3):
    stem, leaf_shape = leaf_paths(stem_length, leaf_length, scale(leaf_width, arc), angle_degrees)
    stem_forward, stem_backward = stem_points(stem, stitch_length)

    leaf_underlay = stripes_along(get_underlay_path(leaf_shape, inset=underlay_inset), repetitions=3,
                                  sampling_function=remove_end(sampling_by_length(stitch_length)),
                                  step_ratio=0.1)
    leaf_satin = satin_along(leaf_shape.inverse(),
                             sampling_function=remove_end(sampling_by_length(satin_spacing)),
                             connect_function=simple_connect)[:-1]

    stitches = [
        stem_forward,
        leaf_underlay,
        leaf_satin,
        stem_backward
    ]
    return np.concatenate(stitches)


def leaf_with_middle_line(stem_length: float, leaf_length: float, leaf_width: float, angle_degrees: float,
                          stitch_length: float, contour_repetitions: int = 1):
    return _leaf(stem_length, leaf_length, leaf_width, angle_degrees, stitch_length, contour_repetitions,
                 middle_line_length=0.7)


def leaf_baseline(length: float, angle: float, arc_length_param: bool):
    baseline = line((0, 0), (length, 0))
    control_points = baseline(sample_by_number(3))
    offset = control_points[1].copy()
    control_points -= offset
    control_points[-2:] = rotate_by_degrees(control_points[-2:], angle)
    control_points += offset

    shape = bezier(control_points)
    direction = bezier_normals(control_points)
    if arc_length_param:
        mapping = arc_length_mapping(shape)
        shape = combine(mapping, shape)
        direction = combine(mapping, direction)

    return shape, direction


def stem_points(stem_path: Path, stitch_length: float):
    stem_1, stem_2 = get_boundaries(stem_path)
    t_stem = sample_by_length(stem_path.length, segment_length=stitch_length)
    stem_forward = stem_1(t_stem)
    stem_backward = inverse(stem_2)(t_stem)
    return stem_forward[:-1], stem_backward


def leaf_paths(stem_length: float, leaf_length: float, leaf_width: Function1D, angle_degrees: float):
    shape, direction = leaf_baseline(length=leaf_length + stem_length, angle=angle_degrees, arc_length_param=True)

    stem_ratio = stem_length / (stem_length + leaf_length)

    stem_shape, leaf_shape = split(shape, [stem_ratio])
    stem_direction, leaf_direction = split(direction, [stem_ratio])

    stem = Path(shape=stem_shape, direction=stem_direction, width=constant(0))
    leaf = Path(shape=leaf_shape, direction=leaf_direction, width=leaf_width)

    return stem, leaf


def _leaf(stem_length: float, leaf_length: float, leaf_width: float, angle_degrees: float,
          stitch_length: float, contour_repetitions: int = 1, middle_line_length: float = 0):
    stem, leaf_shape = leaf_paths(stem_length, leaf_length, scale(leaf_width, arc), angle_degrees)
    leaf_left, leaf_right = get_boundaries(leaf_shape)
    leaf_middle = repeat(middle_line_length, leaf_shape.shape)

    shapes = [
        stem.shape,
        *([leaf_left, inverse(leaf_right)] * contour_repetitions),
        leaf_middle if middle_line_length > 0 else None,
        inverse(leaf_middle) if middle_line_length > 0 else None,
        inverse(stem.shape)
    ]

    running_stitch = partial(running_stitch_on_shape, stitch_length=stitch_length, include_endpoint=False)

    stitches = [running_stitch(shape) for shape in shapes if shape is not None]

    # add end point if it is not the same as the start point
    stitches.append(stem.shape(0))

    return np.concatenate(stitches)
