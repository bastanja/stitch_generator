import numpy as np

from stitch_generator.collection.functions.functions_1d import half_circle
from stitch_generator.collection.stitch_effects.underlay_contour_zigzag import underlay_contour_zigzag
from stitch_generator.framework.path import Path
from stitch_generator.functions.connect_functions import running_stitch_line
from stitch_generator.functions.function_modifiers import scale
from stitch_generator.functions.functions_1d import constant
from stitch_generator.functions.functions_2d import constant_direction
from stitch_generator.sampling.sample_by_length import sample_by_length, sampling_by_length_with_offset
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.path_effects.satin import satin
from stitch_generator.stitch_operations.rotate import rotate_by_degrees


def ellipse_path(width: float, length: float):
    half_length = length / 2
    return Path(shape=line((-half_length, 0), (half_length, 0)), direction=constant_direction(0, -1),
                width=scale(width, half_circle), stroke_alignment=constant(0.5))


def satin_ellipse(width: float, height: float, stitch_length: float, pull_compensation: float = 0,
                  underlay_inset: float = 0.5, underlay_spacing: float = 1.5, satin_spacing: float = 0.2,
                  return_to_start: bool = True):
    inner_path = ellipse_path(width=height - underlay_inset, length=width - underlay_inset)
    outer_path = ellipse_path(width=width + pull_compensation, length=height)

    stitches = []

    if return_to_start:
        stitches.append(outer_path.shape(sample_by_length(height, stitch_length)))
        outer_path = outer_path.inverse()

    underlay_effect = underlay_contour_zigzag(inset=underlay_inset, stitch_length=stitch_length,
                                              spacing=underlay_spacing)
    underlay_stitches = rotate_by_degrees(underlay_effect(inner_path), angle_deg=90)

    satin_effect = satin(
        sampling_function=sampling_by_length_with_offset(segment_length=satin_spacing, offset=0.5),
        connect_function=running_stitch_line(width * 2, include_endpoint=False))
    satin_stitches = satin_effect(outer_path)

    stitches += [underlay_stitches, satin_stitches]
    stitches.append(outer_path.shape(1))
    return np.concatenate(stitches)


def satin_circle(diameter: float, stitch_length: float, pull_compensation: float = 0, underlay_inset: float = 0.5,
                 underlay_spacing: float = 1.5, satin_spacing: float = 0.2, return_to_start: bool = True):
    return satin_ellipse(width=diameter, height=diameter, stitch_length=stitch_length,
                         pull_compensation=pull_compensation, underlay_inset=underlay_inset,
                         underlay_spacing=underlay_spacing, satin_spacing=satin_spacing,
                         return_to_start=return_to_start)
