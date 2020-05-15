import numpy as np

from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import combine
from stitch_generator.functions.functions_1d import linear_interpolation


def function_sequence(functions, lengths=None):
    if not lengths:
        lengths = [estimate_length(f) for f in functions]

    lengths = np.cumsum(lengths).astype(float)
    lengths /= lengths[-1]

    low = 0
    mapped_functions = []
    for idx, f in enumerate(functions):
        high = lengths[idx]
        mapped_functions.append(combine(linear_interpolation(0, 1, low, high), f))
        low = high

    def sequence(v):
        v = np.asarray(v, dtype=float).reshape(-1, 1)
        function_indices = np.argmax(lengths[None, :] >= v, axis=1)
        dimension = len(mapped_functions[0](0).reshape(-1, 1))
        result = np.zeros((len(v), dimension))

        for j in range(len(mapped_functions)):
            result[function_indices == j] = mapped_functions[j](v[function_indices == j])

        return result

    return sequence


if __name__ == "__main__":
    from stitch_generator.functions.functions_2d import line
    from stitch_generator.functions.linspace import samples
    from stitch_generator.functions.functions_1d import constant

    seq = function_sequence((line(0, 10), line(10, 10, 0, 10), line(20, 10, 10, 10)))

    p = samples(30, True)
    print("--- 2D ---")
    print(seq(0.0))
    print(seq(p))

    print("--- 1D ---")
    seq2 = function_sequence((constant(0), linear_interpolation(0,1), constant(1)), (1, 1, 1))
    print(seq2(0.0))
    print(seq2(p))