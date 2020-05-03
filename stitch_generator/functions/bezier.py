import numpy as np


def de_casteljau(control_points: np.ndarray, parameters: np.ndarray) -> (np.ndarray, np.ndarray):
    interpolated_points = control_points
    while len(interpolated_points) > 1:
        new_interpolated_points = []
        for i in range(len(interpolated_points) - 1):
            a = interpolated_points[i]
            b = interpolated_points[i + 1]
            vectors = b - a
            interpolated = a + vectors * parameters[:, None]
            new_interpolated_points.append(interpolated)
        if len(interpolated_points) == 2:
            tangents = vectors
            tangent_lengths = np.linalg.norm(tangents, axis=1, keepdims=True)
            tangents /= tangent_lengths
        interpolated_points = new_interpolated_points

    return interpolated_points[0], tangents
