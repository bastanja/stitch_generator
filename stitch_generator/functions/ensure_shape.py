import numpy as np


def ensure_1d_shape(parameters):
    """
    Converts a list or array into a one-dimensional numpy ndarray
    """
    parameters = np.atleast_1d(parameters)
    parameters = np.squeeze(parameters)
    parameters = np.atleast_1d(parameters)
    return parameters


def ensure_2d_shape(parameters):
    """
    Converts a list or array into a two-dimensional numpy ndarray
    """
    parameters = np.atleast_2d(parameters)
    parameters = np.squeeze(parameters)
    parameters = np.atleast_2d(parameters)
    return parameters
