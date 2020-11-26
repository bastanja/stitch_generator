import numpy as np
from scipy.spatial.ckdtree import cKDTree

from stitch_generator.design_utilities.embroidery_design import EmbroideryDesign
from stitch_generator.design_utilities.parameter import FloatParameter, IntParameter, BoolParameter
from stitch_generator.functions.embroidery_pattern import EmbroideryPattern
from stitch_generator.functions.function_modifiers import multiply, add, combine, inverse
from stitch_generator.functions.functions_1d import linear_interpolation, smoothstep
from stitch_generator.functions.functions_2d import spiral, constant_direction
from stitch_generator.sampling.resample import resample
from stitch_generator.sampling.sample_by_number import sample_by_number
from stitch_generator.stitch_operations.remove_duplicates import remove_duplicates


class Design(EmbroideryDesign):
    def __init__(self):
        EmbroideryDesign.__init__(self, name="elevation", parameters={
            'stitch_length': FloatParameter("Stitch_length", 1, 3, 6),
            'line_distance': FloatParameter("Line_distance", 1, 3, 10),
            'line_repetition': IntParameter("Line Repetition", 1, 2, 3),
            'elevation': FloatParameter("Elevation", -20, 10, 20),
            'max_distance': FloatParameter("Maximum distance", 5, 20, 50),
            'width': FloatParameter("Width", 20, 180, 200),
            'height': FloatParameter("Height", 20, 130, 200),
            'show_path': BoolParameter("Show path", False),
        })

    def get_pattern(self, parameters):
        parameters = self.validate(parameters)
        stitches_per_row = int(round(parameters.width / parameters.stitch_length))
        stitches_per_column = int(round(parameters.height / parameters.line_distance))

        stitch_coordinates = _make_stitches(parameters.width, parameters.height, stitches_per_column, stitches_per_row)

        # adapt grid-y coordinate by distance to the elevation points
        ep = _get_elevation_points(parameters.width, parameters.height)
        tree = cKDTree(ep)

        dist, _ = tree.query(stitch_coordinates)
        dist[dist > parameters.max_distance] = parameters.max_distance
        dist /= parameters.max_distance

        profile = combine(inverse(smoothstep()), linear_interpolation(0, parameters.elevation))
        for line in dist:
            line[:] = profile(line)

        direction = np.ones_like(stitch_coordinates)
        direction[:, :, 1] = -dist

        stitch_coordinates += direction

        # repeat stitch lines
        stitch_coordinates = np.repeat(stitch_coordinates, parameters.line_repetition, axis=1)

        stitches = remove_duplicates(_make_stitch_path(stitch_coordinates))

        pattern = EmbroideryPattern()
        pattern.add_stitches(stitches)

        if parameters.show_path:
            ep -= np.array((0, parameters.elevation)).T
            pattern.add_stitches(resample(ep, parameters.stitch_length), 0x0044FF)

        return pattern


def _make_stitch_path(stitch_coordinates):
    # alternate direction of every second line
    odd = stitch_coordinates[:, 1::2, :]
    odd[:] = np.flipud(odd)

    # turn grid columns and rows into a single row
    stitches = stitch_coordinates.reshape((-1, 1, 2), order='F')
    stitches = stitches[:, 0]
    return stitches


def _make_stitches(width, height, stitches_per_column, stitches_per_row):
    # index 0: x-coordinate in grid
    # index 1: y-coordinate in grid
    # index 3: x and y of grid point
    stitch_coordinates = np.zeros((stitches_per_row, stitches_per_column, 2), dtype=float)
    x_coords = linear_interpolation(0, width)
    y_coords = linear_interpolation(0, height)
    x_samples = x_coords(sample_by_number(stitches_per_row - 1, include_endpoint=True))[:, None]
    y_samples = y_coords(sample_by_number(stitches_per_column - 1, include_endpoint=True))[None, :]
    # set x and y coordinates
    stitch_coordinates[:, :, 0] = x_samples
    stitch_coordinates[:, :, 1] = y_samples
    return stitch_coordinates


def _get_elevation_points(width, height):
    f = spiral(0, 50, turns=2.5)
    f = multiply(f, constant_direction(1.5, 1))
    f = add(f, constant_direction(width / 2, height / 2))
    sp = f(sample_by_number(1000, include_endpoint=True))
    return sp


if __name__ == "__main__":
    Design().cli()
