from stitch_generator.functions.function_modifiers import split
from stitch_generator.functions.types import Function1D, Function2D


class Path:
    def __init__(self, position: Function2D, direction: Function2D, width: Function1D, stroke_alignment: Function1D):
        self.position = position
        self.direction = direction
        self.width = width
        self.stroke_alignment = stroke_alignment

    def split(self, offsets):
        positions = split(self.position, offsets)
        directions = split(self.direction, offsets)
        widths = split(self.width, offsets)
        stroke_alignments = split(self.stroke_alignment, offsets)
        return [Path(*params) for params in zip(positions, directions, widths, stroke_alignments)]

