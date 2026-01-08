from typing import Callable

from .path import Path
from .types import Array2D

StitchEffect = Callable[[Path], Array2D]
