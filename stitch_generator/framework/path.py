from stitch_generator.framework.types import Function1D, Function2D


class Path:
    def __init__(self, shape: Function2D, direction: Function2D, width: Function1D, stroke_alignment: Function1D):
        """
        Creates a Path

        Args:
            shape:            A 2D function that defines the baseline of the path
            direction:        A 2D function that defines the direction along the path. Usually perpendicular to the
                              tangent of the baseline, pointing to the left side of the path
            width:            A 1D function that defines the width of the path
            stroke_alignment: A 1D function that defines how much of the path is left of the baseline. 0 means the left
                              side of the path is equal to the baseline. 1 means that the right side of the path is
                              equal to the baseline. 0.5 means that the path is centered around the baseline.
        """
        self.shape = shape
        self.direction = direction
        self.width = width
        self.stroke_alignment = stroke_alignment
