import numpy as np

from stitch_generator.functions import noise, noise_field

# reference values were generated with pnoise2 from the noise package, which the noise functions used before they
# got their own Perlin noise implementation
_positions_1d = np.array([0, 0.1, 0.25, 0.5, 0.75, 1.0, 2.3, 10.7])


def test_noise_matches_reference_values():
    expected = [
        0.0,
        0.08043266,
        0.03080078,
        -0.1188761,
        -0.10575437,
        -0.26954678,
        -0.23762414,
        0.06500234,
    ]
    assert np.allclose(noise()(_positions_1d), expected, atol=1e-5)


def test_noise_with_parameters_matches_reference_values():
    expected = [
        0.0,
        0.14086325,
        -0.17197257,
        0.12108127,
        0.7575385,
        -0.2449722,
        -0.23819509,
        0.26836249,
    ]
    assert np.allclose(
        noise(octaves=1, angle=45, scale=3)(_positions_1d), expected, atol=1e-5
    )


def test_noise_field_matches_reference_values():
    positions = np.array([[0, 0], [0.2, 0.7], [0.5, 0.5], [1, 0.3]])
    expected = [0.0, -0.01765539, 0.0, 0.03412114]
    assert np.allclose(
        noise_field(-3, -2, 5, 4, octaves=3)(positions), expected, atol=1e-5
    )
