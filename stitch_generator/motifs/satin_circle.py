import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.functions.connect_functions import running_stitch_line
from stitch_generator.functions.function_modifiers import repeat, scale
from stitch_generator.functions.functions_1d import circular_arc, constant
from stitch_generator.functions.functions_2d import constant_direction
from stitch_generator.sampling.sample_by_length import sample_by_length, sampling_by_length_with_offset
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.path_effects.satin import satin
from stitch_generator.collection.stitch_effects.underlay_contour_zigzag import underlay_contour_zigzag


def satin_ellipse(width: float, height: float, stitch_length: float, pull_compensation: float = 0,
                  underlay_inset: float = 0.5, underlay_spacing: float = 1.5, satin_spacing: float = 0.2,
                  return_to_start: bool = True):
    underlay_effect = underlay_contour_zigzag(inset=underlay_inset, stitch_length=stitch_length,
                                              spacing=underlay_spacing)

    satin_effect = satin(
        sampling_function=sampling_by_length_with_offset(segment_length=satin_spacing, offset=0.5),
        connect_function=running_stitch_line(width * 2, include_endpoint=False))

    radius = height / 2

    path = Path(
        shape=line((-radius, 0), (radius, 0)),
        direction=constant_direction(0, -1),
        width=scale(width + pull_compensation, repeat(2, circular_arc, mode='reflect')),
        stroke_alignment=constant(0.5)
    )

    stitches = []
    if return_to_start:
        stitches.append(path.shape(sample_by_length(height, stitch_length)))
        path = path.inverse()
    else:
        stitches.append(path.shape(0))

    stitches += [underlay_effect(path), satin_effect(path)]
    stitches.append(path.shape(1))
    return np.concatenate(stitches)


def satin_circle(diameter: float, stitch_length: float, pull_compensation: float = 0, underlay_inset: float = 0.5,
                 underlay_spacing: float = 1.5, satin_spacing: float = 0.2, return_to_start: bool = True):
    return satin_ellipse(width=diameter, height=diameter, stitch_length=stitch_length,
                         pull_compensation=pull_compensation, underlay_inset=underlay_inset,
                         underlay_spacing=underlay_spacing, satin_spacing=satin_spacing,
                         return_to_start=return_to_start)
