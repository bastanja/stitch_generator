from stitch_generator.functions.types import Function1D, Function2D


class Path:
    def __init__(self, position: Function2D, direction: Function2D, width: Function1D, stroke_alignment: Function1D):
        self.position = position
        self.direction = direction
        self.width = width
        self.stroke_alignment = stroke_alignment
