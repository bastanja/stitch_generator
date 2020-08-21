from stitch_generator.functions.function_modifiers import shift, repeat
from stitch_generator.functions.types import Function1D, Function2D


class Path:
    def __init__(self, position: Function2D, direction: Function2D, width: Function1D, stroke_alignment: Function1D):
        self.position = position
        self.direction = direction
        self.width = width
        self.stroke_alignment = stroke_alignment

    def split(self, offset):
        positions = _split(self.position, offset)
        directions = _split(self.direction, offset)
        widths = _split(self.width, offset)
        stroke_alignments = _split(self.stroke_alignment, offset)
        return [Path(*params) for params in zip(positions, directions, widths, stroke_alignments)]


def _split(function, offset):
    return repeat(offset, function), repeat(1-offset, shift(offset, function))