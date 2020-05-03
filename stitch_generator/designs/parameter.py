import numpy as np
from scipy.interpolate import interp1d


class FloatParameter:
    def __init__(self, label, minimum: float, default: float, maximum: float):
        self.label = label
        self.min = minimum
        self.value = default
        self.max = maximum


class IntParameter:
    def __init__(self, label, minimum: int, default: int, maximum: int):
        self.label = label
        self.min = minimum
        self.value = default
        self.max = maximum


class BoolParameter:
    def __init__(self, label, default: bool):
        self.label = label
        self.value = default


class RampParameter:
    def __init__(self, label, values: np.array):
        self.label = label
        self.value = values

    @property
    def value(self):
        samples = list(self._value_array[0])
        values = list(self._value_array[1])

        # Use cubic interpolation (3) if there are enough samples,
        # otherwise reduce to len(samples) - 1, i.e. quadratic (2) or linear (1)
        interpolation = min(len(samples) - 1, 3)

        f = interp1d(samples, values, kind=interpolation)
        return f

    @value.setter
    def value(self, value_array: np.array):
        self._value_array = value_array

    def get_raw_values(self):
        return list(self._value_array[1])


if __name__ == "__main__":
    values = [0, 1, 1, 1, 1]
    samples = np.linspace(0, 1, num=len(values), endpoint=True)
    r = RampParameter("bla", np.array([samples, values]))
    f = r.get_function()
    v = [f(t / 10).item() for t in range(0, 11)]
    print(v)
