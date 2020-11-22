import numpy as np

from stitch_generator.functions.arc_length_mapping import arc_length_mapping_with_length
from stitch_generator.functions.function_modifiers import combine
from stitch_generator.functions.functions_2d import line, bezier
from stitch_generator.functions.place_motif import place_motif_at
from stitch_generator.sampling.sample_by_length import sample_by_length
from stitch_generator.stitch_effects.rotate import rotate_deg


def straight_line(length: float, stitch_length: float):
    f = line((0, 0), (length, 0))
    forward, back = _sample(f, length, stitch_length)
    return np.vstack((forward, back))


def bent_line(length: float, stitch_length: float, angle_deg):
    f, _ = _bent_line_f(length, angle_deg)
    forward, back = _sample(f, length, stitch_length)
    return np.vstack((forward, back))


def straight_line_with_motif(length: float, stitch_length: float, motif):
    f = line((0, 0), (length, 0))
    forward, back = _sample(f, length, stitch_length)
    return np.vstack((forward[:-1], motif + (length, 0), back))


def bent_line_with_motif(length: float, stitch_length: float, angle_deg, motif):
    f, direction = _bent_line_f(length, angle_deg)
    forward, back = _sample(f, length, stitch_length)
    motif = place_motif_at(position=forward[-1], direction=direction, scale=1, motif=motif, include_endpoint=True)
    return np.vstack((forward[:-1], motif, back))


def _bent_line_f(length: float, angle_deg):
    factor = 0.4
    last_point = rotate_deg(np.array([length, 0], ndmin=2), angle_deg)
    control_points = np.array(((0, 0), (factor * length, 0), last_point[0]))
    direction = (control_points[2] - control_points[1])
    direction /= np.linalg.norm(direction)
    f = bezier(control_points)
    mapping, length = arc_length_mapping_with_length(f)
    f = combine(mapping, f)
    return f, direction


def _sample(f, length: float, stitch_length: float):
    samples = sample_by_length(total_length=length, segment_length=stitch_length, include_endpoint=True)
    stitches = f(samples)
    back = stitches[::-1][1:]
    return stitches, back
