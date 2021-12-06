import numpy as np

from stitch_generator.functions.ensure_shape import ensure_1d_shape


def de_casteljau(control_points: np.ndarray, parameters: np.ndarray) -> (np.ndarray, np.ndarray):
    """
    Subdivides a bezier curve into segments using De Casteljau's algorithm
    Args:
        control_points: The control points of the bezier curve
        parameters: The offsets along the curve (between 0 and 1) where the curve is cut into segments
    Returns:
        The points on the curve at the requested offsets
    """
    if len(parameters) == 0:
        return
    interpolated_points = control_points
    parameters = np.atleast_2d(ensure_1d_shape(parameters)).T
    while len(interpolated_points) > 1:
        new_interpolated_points = []
        for i in range(len(interpolated_points) - 1):
            a = interpolated_points[i]
            b = interpolated_points[i + 1]
            vectors = b - a
            interpolated = a + vectors * parameters
            new_interpolated_points.append(interpolated)
        if len(interpolated_points) == 2:
            tangents = vectors
            tangent_lengths = np.linalg.norm(tangents, axis=1, keepdims=True)
            tangents /= tangent_lengths
        interpolated_points = new_interpolated_points

    return interpolated_points[0], tangents
