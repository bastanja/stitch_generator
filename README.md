# Stitch Generator

Stitch Generator creates stitch patterns for machine embroidery. It converts basic shapes like lines, Bézier curves or
circles to decorative stitch patterns like satin stitches or motif stitches.

## Stitch Effects

Stitch Effects use a Path as input and return an array of stitch coordinates as output.

![stitch effects](https://github.com/bastanja/stitch_generator/raw/main/doc/images/path_stitch_effect_examples.svg "Examples of stitch effects" )

On the left is an example of a path that consists of a cubic Bézier curve with a constant width. On the right there are
examples of stitch effects applied to the path. The dots represent the coordinates of the stitches.

See [List of Stitch Effects](https://github.com/bastanja/stitch_generator/blob/main/doc/list_of_stitch_effects.md)
for an overview over the available stitch effects.

## Decorative Stitches

Stitch Generator provides a collection of decorative stitches. Decorative stitches are stitch effects, too. But they
mostly have a fixed width instead of using the width of the path.

![decorative stitches](https://github.com/bastanja/stitch_generator/raw/main/doc/images/list_of_decorative_stitches.svg "Examples of decorative stitches")

See [List of Decorative Stitches](https://github.com/bastanja/stitch_generator/blob/main/doc/list_of_decorative_stitches.md)
for an overview over the available decorative stitches.

## Subdivision Functions

Stitch Generator provides multiple subdivision functions that can be used to create stitch patterns. This is useful for
subdividing longer lines into stitches, for example when using a meander stitch effect on a path which is wider than a
regular stitch length.

Subdivision functions subdivide a given length into smaller segments. The segments can all have the same length or
varying lengths, and they can be shifted by an offset in each line.

In this example subdivision functions are used in combination with a meander stitch effect to create different stitch
patterns:

![subdivision](https://github.com/bastanja/stitch_generator/raw/main/doc/images/meander_subdivision_example.svg "Examples of subdivision patterns")

See [Subdivision Functions](https://github.com/bastanja/stitch_generator/blob/main/doc/subdivision_functions.md) for an
overview over the available subdivision functions.

# Usage

## Installation

### Install from pypi

The recommended way to install Stitch Generator is using pypi:

```
> pip install stitch_generator
```

### Install from local git checkout

Alternatively, Stitch Generator can be installed from a local git checkout:

```
> git clone git@github.com:bastanja/stitch_generator.git
> cd stitch_generator
> pip install .
```

## Creating Paths

In order to use stitch effects, you first need to create a path.
See [Paths](https://github.com/bastanja/stitch_generator/blob/main/doc/paths.md) for an overview over paths and how to
create them. Example for creating a simple linear path:

```python
from stitch_generator.shapes.line import line
from stitch_generator.framework.path import Path
from stitch_generator.functions.functions_1d import constant

path = Path(*line(origin=(-50, 0), to=(50, 0)), width=constant(15))
```

## Using Stitch Effects

### Stitch effect from collection

Example for using a stitch effect from the Stitch Generator collection

```python
from stitch_generator.collection.stitch_effects.stitch_effects import stitch_effect_meander
from stitch_generator.shapes.line import line
from stitch_generator.framework.path import Path
from stitch_generator.functions.functions_1d import constant

# create a path
path = Path(*line(origin=(-50, 0), to=(50, 0)), width=constant(15))

# apply the stitch effect
stitches = stitch_effect_meander(path)
```

### Custom stitch effect

Example for using a custom stitch effect

```python
from stitch_generator.stitch_effects.path_effects.satin import satin
from stitch_generator.shapes.line import line
from stitch_generator.framework.path import Path
from stitch_generator.functions.functions_1d import constant
from stitch_generator.subdivision.subdivide_by_length import regular

# create a path
path = Path(*line(origin=(-50, 0), to=(50, 0)), width=constant(15))

# create a satin stitch effect
stitch_effect = satin(spacing_function=regular(2), line_subdivision=regular(4))

# apply the stitch effect
stitches = stitch_effect(path)
```

See [List of Stitch Effects](https://github.com/bastanja/stitch_generator/blob/main/doc/list_of_stitch_effects.md) for
an overview over the available stitch effects.

### Decorative stitch from collection

Example for using a decorative stitch from the Stitch Generator collection

```python
from stitch_generator.collection.stitch_effects.decorative_stitches import arrow_chain
from stitch_generator.shapes.line import line
from stitch_generator.framework.path import Path
from stitch_generator.functions.functions_1d import constant

# create a path
path = Path(*line(origin=(-50, 0), to=(50, 0)), width=constant(15))

# create the stitch_effect
stitch_effect = arrow_chain(arrow_width=8, arrow_length=2, arrow_spacing=2)

# apply the stitch effect
stitches = stitch_effect(path)
```

See [List of Decorative Stitches](https://github.com/bastanja/stitch_generator/blob/main/doc/list_of_decorative_stitches.md)
for an overview over the available decorative stitches.

## Using the stitches

The result of applying a stitch effect to a path are stitch coordinates. `stitches` is a two-dimensional numpy ndarray.
Dimension 0 is the number of stitches. Dimension 1 contains the x and y coordinate of each stitch:

```
>>> stitches
array([[  1.,   5.],
       [  2.,  -5.],
       [  3.,   5.],
       ...,
       [ 98.,  -5.],
       [ 99.,   5.],
       [100.,  -5.]])
```

Stitch Generator has no functionality to write embroidery files. For writing embroidery files,
[pyembroidery](https://pypi.org/project/pyembroidery/) is recommended.

Note that the stitches from StitchGenerator are in millimeters, but pyembroidery expects 1/10 mm. Therefore, the
stitches need to be scaled.

Example how to create a pyembroidery EmbPattern with stitches from Stitch Generator:

```python
from pyembroidery import EmbPattern

scale_factor = 10  # convert from millimeters to embroidery file scale 1/10 mm

scaled_stitches = stitches * scale_factor
pattern = EmbPattern()
pattern.add_block(scaled_stitches.tolist(), "red")
```

See pyembroidery documentation for information how to write an EmbPattern to different file formats.
