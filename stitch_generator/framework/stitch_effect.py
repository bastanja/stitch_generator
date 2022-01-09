from typing import Callable

from stitch_generator.framework.path import Path
from stitch_generator.framework.types import Array2D

StitchEffect = Callable[[Path], Array2D]
