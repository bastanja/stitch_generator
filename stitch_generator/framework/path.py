from stitch_generator.framework.types import Function1D, CoordinateFunction


class Path:
    """
    A Path represents a parametric path with shape, direction, width, and stroke alignment.
    """
    def __init__(
        self,
        shape: CoordinateFunction,
        direction: CoordinateFunction,
        width: Function1D,
        stroke_alignment: Function1D,
    ):
        """
        Creates a Path

        Args:
            shape:            A function that returns coordinate points and defines the baseline of the path.
                              Should accept parameters in [0, 1] and return coordinate arrays.
            direction:        A function that returns coordinate vectors and defines the direction along the path.
                              Usually perpendicular to the tangent of the baseline, pointing to the left side of the path.
                              Should return normalized direction vectors.
            width:            A 1D function that defines the width of the path
            stroke_alignment: A 1D function that defines how much of the path is left of the baseline. 0 means the left
                              side of the path is equal to the baseline. 1 means that the right side of the path is
                              equal to the baseline. 0.5 means that the path is centered around the baseline.
        """
        self.shape = shape
        self.direction = direction
        self.width = width
        self.stroke_alignment = stroke_alignment
