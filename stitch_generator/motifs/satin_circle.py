import numpy as np

from stitch_generator.functions.connect_functions import running_stitch_line
from stitch_generator.functions.function_modifiers import repeat, scale
from stitch_generator.functions.functions_1d import circular_arc, constant
from stitch_generator.functions.functions_2d import constant_direction
from stitch_generator.path.path import Path
from stitch_generator.sampling.sample_by_length import sample_by_length, sampling_by_length_with_offset
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.satin import satin
from stitch_generator.stitch_effects.underlay import contour_zigzag_underlay


def satin_circle(diameter: float, stitch_length: float, pull_compensation: float = 0, underlay_inset: float = 0.5,
                 underlay_spacing: float = 1.5, satin_spacing: float = 0.2, return_to_start: bool = True):
    underlay_effect = contour_zigzag_underlay(inset=underlay_inset, stitch_length=stitch_length,
                                              spacing=underlay_spacing)

    satin_effect = satin(
        sampling_function=sampling_by_length_with_offset(segment_length=satin_spacing, offset=0.5),
        connect_function=running_stitch_line(diameter * 2, include_endpoint=False))

    path = Path(
        position=line((0, 0), (diameter, 0)),
        direction=constant_direction(0, -1),
        width=scale(diameter + pull_compensation, repeat(2, circular_arc(), mode='reflect')),
        stroke_alignment=constant(0.5)
    )

    stitches = []
    if return_to_start:
        middle_run = lambda path: path.position(
            sample_by_length(path.length, stitch_length, include_endpoint=False))
        stitches.append(middle_run(path))
        path = path.inverse()
    else:
        stitches.append(path.position(0))

    stitches += [underlay_effect(path), satin_effect(path)]
    stitches.append(path.position(1))
    return np.concatenate(stitches)
