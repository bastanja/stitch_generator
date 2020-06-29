from stitch_generator.designs import elevation
from stitch_generator.designs import noise_spiral
from stitch_generator.designs import variable_running_stitch
from stitch_generator.designs import waves

designs = {
    'Waves': waves.Design,
    'Noise spiral': noise_spiral.Design,
    'Elevation': elevation.Design,
    'Running Stitch': variable_running_stitch.Design,
}
