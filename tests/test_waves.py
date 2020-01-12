from designs.waves import Waves
from file_io.embroidery_export import export_vp3


def test_get_pattern():
    waves = Waves()
    pattern = waves.get_pattern()

    assert pattern.number_of_stitches > 0
    export_vp3(pattern, "waves.vp3")
