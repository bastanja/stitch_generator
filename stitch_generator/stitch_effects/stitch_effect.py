from typing import Callable

from stitch_generator.path.path import Path
from stitch_generator.utilities.types import Array2D

StitchEffect = Callable[[Path], Array2D]