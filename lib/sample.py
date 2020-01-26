from functools import partial
import numpy as np


def sample(function, number_of_samples: int, include_endpoint: bool = True):
    if include_endpoint:
        number_of_samples += 1
    v = np.linspace(0, 1, num=number_of_samples, endpoint=include_endpoint)
    return np.array([function(t) for t in v])


def _generator(function, number_of_samples: int, include_endpoint: bool = True):
    step = 1 / number_of_samples

    for i in range(number_of_samples):
        yield function(step * i)

    if include_endpoint:
        yield function(1)


def sample_generator(number_of_samples: int, include_endpoint: bool = True):
    return partial(_generator, number_of_samples=number_of_samples, include_endpoint=include_endpoint)
