import numpy as np


def sample(function, number_of_samples: int = 100, include_endpoint: bool = True):
    if not include_endpoint:
        number_of_samples -= 1
    v = np.linspace(0, 1, num=number_of_samples, endpoint=include_endpoint)
    return [function(t) for t in v]
