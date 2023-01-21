from typing import Tuple

from stitch_generator.collection.functions.functions_1d import half_circle
from stitch_generator.collection.stitch_effects.underlays import underlay_contour_zigzag
from stitch_generator.collection.subdivision.tatami import tatami_3_1
from stitch_generator.framework.path import Path
from stitch_generator.functions.function_modifiers import scale
from stitch_generator.functions.functions_1d import constant
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.path_effects.meander import meander
from stitch_generator.stitch_effects.path_effects.zigzag import zigzag, double_zigzag
from stitch_generator.stitch_operations.connect import connect
from stitch_generator.stitch_operations.rotate import rotate_90
from stitch_generator.subdivision.subdivide_by_length import subdivide_by_length, subdivision_by_length_with_offset, \
    regular
from stitch_generator.subdivision.subdivision_modifiers import add_end, add_start, alternate_direction


def satin_ellipse(width: float, height: float, stitch_length: float, pull_compensation: float = 0,
                  underlay_inset: float = 0.5, underlay_spacing: float = 1.5, satin_spacing: float = 0.2,
                  return_to_start: bool = False):
    # create stitch effects
    underlay_effect = double_zigzag(spacing_function=regular(underlay_spacing))
    zigzag_effect = zigzag(spacing_function=subdivision_by_length_with_offset(segment_length=satin_spacing, offset=0.5))

    return _satin_ellipse(width=width, height=height, stitch_length=stitch_length, pull_compensation=pull_compensation,
                          underlay_inset=underlay_inset, return_to_start=return_to_start,
                          underlay_effect=underlay_effect, top_effect=zigzag_effect)


def satin_circle(diameter: float, stitch_length: float = 3, pull_compensation: float = 0, underlay_inset: float = 0.5,
                 underlay_spacing: float = 1.5, satin_spacing: float = 0.2, return_to_start: bool = True):
    return satin_ellipse(width=diameter, height=diameter, stitch_length=stitch_length,
                         pull_compensation=pull_compensation, underlay_inset=underlay_inset,
                         underlay_spacing=underlay_spacing, satin_spacing=satin_spacing,
                         return_to_start=return_to_start)


def tatami_ellipse(width: float, height: float, stitch_length: float = 3, pull_compensation: float = 0,
                   underlay_inset: float = 0.5, underlay_spacing: float = 1.5, satin_spacing: float = 0.2,
                   return_to_start: bool = False):
    # create stitch effects
    underlay_effect = _underlay_effect(stitch_length=stitch_length, line_spacing=underlay_spacing)
    line_subdivision = add_start(add_end(alternate_direction(tatami_3_1(segment_length=5))))
    satin_effect = meander(spacing_function=subdivision_by_length_with_offset(segment_length=satin_spacing, offset=0.5),
                           line_subdivision=line_subdivision, join_ends=True)

    return _satin_ellipse(width=width, height=height, stitch_length=stitch_length, pull_compensation=pull_compensation,
                          underlay_inset=underlay_inset, return_to_start=return_to_start,
                          underlay_effect=underlay_effect, top_effect=satin_effect)


def tatami_circle(diameter: float, stitch_length: float, pull_compensation: float = 0, underlay_inset: float = 0.5,
                  underlay_spacing: float = 1.5, satin_spacing: float = 0.2, return_to_start: bool = False):
    return tatami_ellipse(width=diameter, height=diameter, stitch_length=stitch_length,
                          pull_compensation=pull_compensation, underlay_inset=underlay_inset,
                          underlay_spacing=underlay_spacing, satin_spacing=satin_spacing,
                          return_to_start=return_to_start)


def ellipse_path(width: float, height: float):
    half_length = height / 2
    shape, direction = line((0, -half_length), (0, half_length))
    return Path(shape=shape, direction=direction, width=scale(width, half_circle), stroke_alignment=constant(0.5))


def _paths(width: float, height: float, underlay_inset: float, pull_compensation: float) -> Tuple[Path, Path]:
    inner_path = ellipse_path(width=height - underlay_inset, height=width - underlay_inset)
    outer_path = ellipse_path(width=width + pull_compensation, height=height)
    return inner_path, outer_path


def _underlay_effect(stitch_length, line_spacing):
    return underlay_contour_zigzag(inset=0, stitch_length=stitch_length, spacing=line_spacing)


def _satin_ellipse(width: float, height: float, stitch_length: float, pull_compensation: float, underlay_inset: float,
                   return_to_start: bool, underlay_effect, top_effect):
    # create paths
    inner_path, outer_path = _paths(width, height, underlay_inset, pull_compensation)

    # create stitches
    stitches = []

    if return_to_start:
        # add line to the end of the outer shape and inverse the outer path in order to stitch it backwards
        stitches.append(outer_path.shape(subdivide_by_length(height, stitch_length)))
        outer_path = outer_path.inverse()
    else:
        # add the first point of the outer path
        stitches.append(outer_path.shape(0))

    stitches.append(rotate_90(underlay_effect(inner_path)))
    stitches.append(top_effect(outer_path))
    stitches.append(outer_path.shape(1))

    # combine collected stitches
    return connect(stitches, line_subdivision=regular(stitch_length))
