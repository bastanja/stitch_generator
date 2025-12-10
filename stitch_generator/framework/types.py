from typing import Callable, Union, List, Tuple

import numpy as np
from numpy.typing import NDArray

# Array1D: 1D array with shape (N,) containing scalar values
Array1D = NDArray[np.float64]

# Array2D: 2D array with shape (N, 2) where each row is a 2D point (x, y)
# Commonly used for stitch coordinates
Array2D = NDArray[np.float64]

# Array3D: 3D array with shape (N, 3) where each row is a 3D point (x, y, z)
Array3D = NDArray[np.float64]

Function1D = Callable[[Union[float, Array1D]], Array1D]
Function2D = Callable[[Union[float, Array1D]], Array2D]
Function3D = Callable[[Union[float, Array1D]], Array3D]

# Type alias for functions that return coordinate points (2D or 3D)
# Used for shape and direction functions that can work with both 2D and 3D coordinates
CoordinateFunction = Union[Function2D, Function3D]

# Type alias for parameters (single float or array of floats)
Parameters = Union[float, Array1D]

# Type alias for coordinate arrays (2D or 3D)
Coordinates = Union[Array2D, Array3D]

# Type alias for direction arrays (2D or 3D)
Direction = Union[Array2D, Array3D]

# Type alias for any function type (1D, 2D, or 3D)
AnyFunction = Union[Function1D, Function2D, Function3D]

# A function that is called with a length value and returns an array of floats between 0 and 1
SubdivisionFunction = Callable[[float], Array1D]
