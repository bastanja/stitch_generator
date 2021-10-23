import numpy as np
import scipy.interpolate


class FloatParameter:
    """
    A floating point number parameter for an EmbroideryDesign. Has a default value, an allowed minimum and allowed
    maximum value. If the value passed to the StitchDesign exceeds the allowed range, it will be clamped to the nearest
    allowed value.
    """

    def __init__(self, label, minimum: float, default: float, maximum: float):
        self.label = label
        self.min = minimum
        self.value = default
        self.max = maximum

    def evaluate(self, value: float):
        return _clamp(self.min, self.max, value)

    def get_description(self):
        return f"{self.label}: Float between {self.min} and {self.max}, default is {self.value}"

    @staticmethod
    def expected_type():
        return float


class IntParameter:
    """
    An integer number parameter for an EmbroideryDesign. Has a default value, an allowed minimum and allowed maximum
    value. If the value passed to the StitchDesign exceeds the allowed range, it will be clamped to the nearest allowed
    value.
    """

    def __init__(self, label, minimum: int, default: int, maximum: int):
        self.label = label
        self.min = minimum
        self.value = default
        self.max = maximum

    def evaluate(self, value: int):
        return _clamp(self.min, self.max, value)

    def get_description(self):
        return f"{self.label}: Integer between {self.min} and {self.max}, default is {self.value}"

    @staticmethod
    def expected_type():
        return int


class BoolParameter:
    """
    A boolean parameter for a EmbroideryDesign with a default value.
    """

    def __init__(self, label, default: bool):
        self.label = label
        self.value = default

    def evaluate(self, value: bool):
        if value:
            return True
        return False

    def get_description(self):
        return f"{self.label}: Bool, default is {self.value}"

    @staticmethod
    def expected_type():
        return bool


class RampParameter:
    """
    A parameter for an EmbroideryDesign that represents a 1DFunction. The 1DFunction returned by this parameter is an
    interpolation that goes through a given set of control points.

    This parameter is not available from the command line interface.
    """

    def __init__(self, label, control_points: np.ndarray):
        self.label = label
        self.control_points = np.asarray(control_points)
        self.value = self.function_from_control_points()

    def function_from_control_points(self):
        return scipy.interpolate.PchipInterpolator(self.control_points[:, 0], self.control_points[:, 1])

    def evaluate(self, function_1d):
        return function_1d


def _clamp(low, high, value):
    value = min(high, value)
    value = max(low, value)
    return value
