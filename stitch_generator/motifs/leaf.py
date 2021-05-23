from functools import partial
from typing import Callable

import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.functions.arc_length_mapping import arc_length_mapping
from stitch_generator.functions.connect_functions import simple_connect
from stitch_generator.functions.function_modifiers import combine, split, scale, inverse
from stitch_generator.functions.functions_1d import constant, arc
from stitch_generator.functions.get_boundaries import get_boundaries
from stitch_generator.functions.get_underlay_path import get_underlay_path
from stitch_generator.sampling.sample_by_length import sample_by_length, sampling_by_length
from stitch_generator.sampling.sample_by_number import sample_by_number
from stitch_generator.shapes.bezier import bezier, bezier_normals
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.utilities.satin import satin_along
from stitch_generator.stitch_effects.utilities.stripes import stripes_along
from stitch_generator.stitch_operations.rotate import rotate_by_degrees
from stitch_generator.utilities.types import Function1D


def leaf(stem_length: float, leaf_length: float, leaf_width: float, angle_degrees: float, stitch_length: float):
    get_baseline = partial(get_curve, length=leaf_length + stem_length, angle=angle_degrees, arc_length_param=True)

    stem_ratio = stem_length / (stem_length + leaf_length)
    stem, leaf_shape = get_leaf_shape(get_baseline, stem_ratio, scale(leaf_width, arc))

    stem_1, stem_1 = get_boundaries(stem)
    t_stem = sample_by_length(stem_length, segment_length=stitch_length, include_endpoint=False)

    leaf_1, leaf_2 = get_boundaries(leaf_shape)
    t_leaf = sample_by_length(leaf_length, segment_length=stitch_length, include_endpoint=False)

    stitches = [
        stem_1(t_stem),
        leaf_1(t_leaf),
        inverse(leaf_2)(t_leaf),
        inverse(stem_1)(t_stem),
        stem_1(0)
    ]
    return np.concatenate(stitches)


def satin_leaf(stem_length: float, leaf_length: float, leaf_width: float, angle_degrees: float, stitch_length: float,
               satin_spacing: float = 0.2, underlay_inset: float = 0.3):
    get_baseline = partial(get_curve, length=leaf_length + stem_length, angle=angle_degrees, arc_length_param=True)

    stem_ratio = stem_length / (stem_length + leaf_length)
    stem, leaf_shape = get_leaf_shape(get_baseline, stem_ratio, scale(leaf_width, arc))

    stem_1, stem_1 = get_boundaries(stem)
    t_stem = sample_by_length(stem_length, segment_length=stitch_length, include_endpoint=False)

    leaf_underlay = stripes_along(get_underlay_path(leaf_shape, inset=underlay_inset), repetitions=3,
                                  sampling_function=sampling_by_length(stitch_length, include_endpoint=False),
                                  step_ratio=0.1)
    leaf_satin = satin_along(leaf_shape.inverse(),
                             sampling_function=sampling_by_length(satin_spacing, include_endpoint=False),
                             connect_function=simple_connect)[:-1]

    stitches = [
        stem_1(t_stem),  # stem forward
        leaf_underlay,
        leaf_satin,
        inverse(stem_1)(t_stem),  # stem backward
        stem_1(0)  # last point of stem
    ]
    return np.concatenate(stitches)


def get_curve(length: float, angle: float, arc_length_param: bool):
    baseline = line((0, 0), (length, 0))
    control_points = baseline(sample_by_number(3, include_endpoint=True))
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


def get_leaf_shape(get_baseline: Callable, stem_ratio: float, leaf_width: Function1D):
    shape, direction = get_baseline()
    stem_shape, leaf_shape = split(shape, [stem_ratio])
    stem_direction, leaf_direction = split(direction, [stem_ratio])

    stem = Path(shape=stem_shape, direction=stem_direction, width=constant(0))
    leaf = Path(shape=leaf_shape, direction=leaf_direction, width=leaf_width)

    return stem, leaf
