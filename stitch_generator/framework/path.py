import numpy as np

from stitch_generator.framework.types import Function1D, Function2D
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import split, inverse, mix
from stitch_generator.functions.functions_1d import constant


class Path:
    def __init__(self, shape: Function2D, direction: Function2D, width: Function1D = constant(1),
                 stroke_alignment: Function1D = constant(0.5)):
        """
        Creates a Path

        Args:
            shape:            A 2D function that defines the base line of the path
            direction:        A 2D function that defines the direction along the path. Usually perpendicular to the
                              tangent of the base line, pointing to the left side of the path
            width:            A 1D function that defines the width of the path
            stroke_alignment: A 1D function that defines how much of the path is left of the base line. 0 means the left
                              side of the path is equal to the base line. 1 means that the right side of the path is
                              equal to the base line. 0.5 means that the path is centered around the base line.
        """
        self.shape = shape
        self.direction = direction
        self.width = width
        self.stroke_alignment = stroke_alignment

    def split(self, offsets):
        """
        Splits a path at the given offsets

        Args:
            offsets: Split locations in the range [0, 1]

        Returns:
            A list of paths, from which each one represents the section of the original path between two offsets
        """
        shapes = split(self.shape, offsets)
        directions = split(self.direction, offsets)
        widths = split(self.width, offsets)
        stroke_alignments = split(self.stroke_alignment, offsets)
        return [Path(*params) for params in zip(shapes, directions, widths, stroke_alignments)]

    def inverse(self):
        """
        Reverses the direction of the path

        Returns:
            The reversed path
        """
        return self.apply_modifier(inverse)

    def apply_modifier(self, function_modifier):
        """
        Applies a function modifier to all members of the Path
        Args:
            function_modifier: A function that can be applied to 1DFunctions and 2DFunctions and returns a function of
                               the same type

        Returns:
            A Path where the function_modifier is applied to all members
        """
        shape = function_modifier(function=self.shape)
        direction = function_modifier(function=self.direction)
        width = function_modifier(function=self.width)
        stroke_alignment = function_modifier(function=self.stroke_alignment)
        return Path(shape, direction, width, stroke_alignment)

    @property
    def length(self):
        return estimate_length(self.shape)

    @property
    def is_circular(self):
        shape_start_end_equal = np.all(np.isclose(self.shape(0), self.shape(1)))
        direction_start_end_equal = np.all(np.isclose(self.direction(0), self.direction(1)))
        return shape_start_end_equal and direction_start_end_equal


def path_from_boundaries(left, right, alignment=constant(0.5)):
    position = mix(left, right, alignment)

    def width(t):
        return np.linalg.norm(left(t) - right(t))

    def direction(t):
        return (left(t) - right(t)) / width(t)

    return Path(shape=position, direction=direction, width=width, stroke_alignment=alignment)
