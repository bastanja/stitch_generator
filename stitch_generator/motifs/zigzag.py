from stitch_generator.sampling.sample_by_number import sampling_by_number
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.utilities.zigzag import zigzag_between


def zigzag(width: float, height: float, repetitions: int, flip: bool = False):
    half_width = width / 2
    half_height = height / 2

    if flip:
        half_height = -half_height

    f1 = line((-half_width, -half_height), (half_width, -half_height))
    f2 = line((-half_width, half_height), (half_width, half_height))

    return zigzag_between(f1, f2, sampling_by_number(repetitions, include_endpoint=True), width)
