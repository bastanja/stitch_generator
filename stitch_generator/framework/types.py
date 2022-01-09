from typing import Callable, Union, List, Tuple

import numpy as np

Array1D = np.ndarray
Array2D = np.ndarray
Array3D = np.ndarray

Point = Union[Tuple[float], List[float], np.ndarray]

Function1D = Callable[[Union[float, Array1D]], Array1D]
Function2D = Callable[[Union[float, Array1D]], Array2D]
Function3D = Callable[[Union[float, Array1D]], Array3D]

# A function that is called with a length value and returns an array of floats between 0 and 1
SamplingFunction = Callable[[float], Array1D]

# A function that is called with a start and end point and returns an Array2D of points starting at the start point and
# ending at the end point
ConnectFunction = Callable[[Point, Point], Array2D]
