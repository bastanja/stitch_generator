from typing import Callable

import numpy as np

Array1D = np.ndarray
Array2D = np.ndarray

Function1D = Callable[[Array1D], Array1D]
Function2D = Callable[[Array1D], Array2D]
