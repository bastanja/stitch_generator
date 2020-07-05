import numpy as np
import scipy.interpolate


def _clamp(low, high, value):
    value = min(high, value)
    value = max(low, value)
    return value


class FloatParameter:
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
    def __init__(self, label, control_points: np.ndarray):
        self.label = label
        self.control_points = np.asarray(control_points)
        self.value = self.function_from_control_points()

    def function_from_control_points(self):
        return scipy.interpolate.PchipInterpolator(self.control_points[:, 0], self.control_points[:, 1])

    def evaluate(self, function_1d):
        return function_1d


class ControlPointsParameter:
    def __init__(self, control_points):
        self.value = np.array(control_points, dtype=float)


if __name__ == "__main__":
    values = [0, 1, 1, 1, 1]
    samples = np.linspace(0, 1, num=len(values), endpoint=True)
    control_points = np.array([samples, values]).T

    r = RampParameter("bla", control_points)
    f = r.value
    v = [f(t / 10).item() for t in range(0, 11)]
    print(v)
