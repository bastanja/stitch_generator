from stitch_generator.functions.function_modifiers import shift, repeat
from stitch_generator.functions.types import Function1D, Function2D


class Path:
    def __init__(self, position: Function2D, direction: Function2D, width: Function1D, stroke_alignment: Function1D):
        self.position = position
        self.direction = direction
        self.width = width
        self.stroke_alignment = stroke_alignment

    def split(self, offsets):
        positions = _split(self.position, offsets)
        directions = _split(self.direction, offsets)
        widths = _split(self.width, offsets)
        stroke_alignments = _split(self.stroke_alignment, offsets)
        return [Path(*params) for params in zip(positions, directions, widths, stroke_alignments)]


def _split(function, offsets):
    try:
        offsets = offsets.tolist()  # convert np.ndarray to list
    except AttributeError:
        offsets = list(offsets)  # make sure we have a list

    combined = [0] + offsets + [1]

    return  [repeat(o2 - o1, shift(o1, function)) for o1, o2 in zip(combined, combined[1:])]
