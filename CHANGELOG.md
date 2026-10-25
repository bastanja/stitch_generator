# Changelog

## 1.0.1 (unreleased)

### Changes

- The dependency on the `noise` package was removed. The noise functions (`noise`, `noise_vectors`, `noise_field`)
  and the `scribble` stitch effect now use a built-in numpy implementation of Perlin noise, so no C compiler is needed
  anymore. It produces the same values as before (up to float precision). The `stitch_generator[noise]` extra still
  exists, but is empty.
- `variable_running_stitch` is faster, especially for width profiles with many changes (up to about 15 times faster
  for noisy profiles). It now samples the shape more densely to estimate its length, so the stitch length is more
  accurate for wiggly shapes. This can slightly change the number of stitches.
- `variable_underlay` is faster, especially for paths whose width changes often (about 7 to 14 times faster). The
  resulting stitches are unchanged.
- `satin` and `double_satin` no longer stitch each zigzag corner twice. The stitch path is unchanged, but the
  resulting stitches contain fewer points.

### Fixes

- `path_from_boundaries` returned a path whose left and right sides were swapped. The path's direction now matches the
  `left` and `right` arguments, so `get_boundaries` returns the original boundaries.
- `meander` failed when the spacing function returned no value or a single value, e.g. on short paths.
- `subdivide_by_length_with_offset` and `subdivision_by_length_with_offset` scaled the offset by the requested segment
  length instead of the actual spacing of the values, which is rounded to fit the total length. The values were
  shifted whenever the total length was not a multiple of the segment length (e.g. not centered for `offset=0.5`), and
  for lengths shorter than the segment length they were placed beyond the end (greater than 1). This changes the
  stitches of effects using these functions, e.g. `satin_circle` and some decorative stitches.
- `zigzag`, `double_zigzag`, `satin` and `double_satin` failed when the spacing function returned fewer than two
  values. They now zigzag once from the start to the end of the path.
- `tile_motif` returned no stitches for paths shorter than half the motif length. It now places at least one motif.
- `motif_chain` failed when no motif positions were placed on the path.
- `motif_to_segments` failed for empty motifs or when a motif's start and end point coincide.

## 1.0.0 (2026-10-14)

### Breaking changes

- Python 3.10 or newer is required. Support for Python 3.7, 3.8 and 3.9 was dropped.
- `Path` no longer exposes member methods such as `split`, `inverse`, `apply_modifier`, `length`, and `is_circular`.
- `Path(...)` now requires explicit `width` and `stroke_alignment` arguments (default values were removed).
- Several function modifiers were renamed (see table below).
- The `noise` package is now an optional dependency. Install it with `pip install stitch_generator[noise]` to use the
  noise functions (`noise`, `noise_vectors`, `noise_field`) and the `scribble` stitch effect.

### Module interface exports

Module interfaces are now explicitly exported via `__init__.py` package interfaces.
For example, `framework` now exports `Path` directly, so this file-based import:

    from stitch_generator.framework.path import Path

is replaced by:

    from stitch_generator.framework import Path

The same style applies to other module interfaces such as
`stitch_generator.functions`, `stitch_generator.helpers`, `stitch_generator.shapes`,
`stitch_generator.subdivision`, and `stitch_generator.stitch_operations`.

### Path interface changes

`Path` is now a plain container class. Behavior moved to module-level helper
functions, mainly in `stitch_generator.helpers.path_operations`.
For example:

    parts = path.split([0.5])

is replaced by:

    parts = split_path(path, [0.5])

The default constructor parameters were removed. You must now pass all arguments:
`shape`, `direction`, `width`, and `stroke_alignment`.

### Reorganization of helper modules

- `add_gap` moved from `stitch_generator.functions.add_gap` to `stitch_generator.helpers.add_gap`.
- `subdivide_line` moved from `stitch_generator.stitch_effects.utilities.subdivide_line` to `stitch_generator.helpers.subdivide_line`.

### Modifier function renaming

Several function modifiers were renamed:

| Old name | New name           |
| -------- | ------------------ |
| nearest  | clamp              |
| chain    | compose            |
| add      | add_functions      |
| subtract | subtract_functions |
| multiply | multiply_functions |
| divide   | divide_functions   |
| maximum  | max_functions      |
| minimum  | min_functions      |

### Migration from 0.1.0

- Replace file-based imports with module interface imports where possible.
- Refactor `Path` member method calls to helper-function calls.
- Update renamed function modifiers using the table above.
- Update moved imports for `add_gap` and `subdivide_line`.
- Run tests to catch API usage and validation issues.

### Import replacement:

| Before | After |
| ------ | ----- |
| `from stitch_generator.framework.path import Path` | `from stitch_generator.framework import Path` |
| `from stitch_generator.framework.stitch_effect import StitchEffect` | `from stitch_generator.framework import StitchEffect` |
| `from stitch_generator.framework.types import Function1D, Function2D` | `from stitch_generator.framework import Function1D, Function2D` |
| `from stitch_generator.functions.functions_1d import constant` | `from stitch_generator.functions import constant` |
| `from stitch_generator.functions.function_modifiers import repeat, chain, add, subtract, multiply, divide` | `from stitch_generator.functions import repeat, compose, add_functions, subtract_functions, multiply_functions, divide_functions` |
| `from stitch_generator.functions.add_gap import add_gap_to_path` | `from stitch_generator.helpers.add_gap import add_gap_to_path` |
| `from stitch_generator.stitch_effects.utilities.subdivide_line import subdivide_line` | `from stitch_generator.helpers.subdivide_line import subdivide_line` |
| `from stitch_generator.shapes.line import line_shape` | `from stitch_generator.shapes import line_shape` |
| `from stitch_generator.subdivision.subdivide_by_number import subdivision_by_number` | `from stitch_generator.subdivision import subdivision_by_number` |
| `from stitch_generator.stitch_operations.rotate import rotate_by_degrees` | `from stitch_generator.stitch_operations import rotate_by_degrees` |

### Stitch effect import replacement:

| Before | After |
| ------ | ----- |
| `from stitch_generator.stitch_effects.path_effects.lattice import lattice` | `from stitch_generator.stitch_effects.path_effects import lattice` |
| `from stitch_generator.stitch_effects.path_effects.contour import contour` | `from stitch_generator.stitch_effects.path_effects import contour` |
| `from stitch_generator.stitch_effects.path_effects.zigzag import zigzag, simple_zigzag` | `from stitch_generator.stitch_effects.path_effects import zigzag, simple_zigzag` |
| `from stitch_generator.stitch_effects.path_effects.satin import satin, simple_satin` | `from stitch_generator.stitch_effects.path_effects import satin, simple_satin` |
| `from stitch_generator.stitch_effects.shape_effects.running_stitch import running_stitch` | `from stitch_generator.stitch_effects.shape_effects import running_stitch` |
| `from stitch_generator.stitch_effects.shape_effects.variable_running_stitch import variable_running_stitch` | `from stitch_generator.stitch_effects.shape_effects import variable_running_stitch` |
| `from stitch_generator.stitch_effects.shape_effects.motif_chain import motif_chain` | `from stitch_generator.stitch_effects.shape_effects import motif_chain` |
| `from stitch_generator.stitch_effects.shape_effects.motif_to_segments import motif_to_segments` | `from stitch_generator.stitch_effects.shape_effects import motif_to_segments` |

## 0.1.0

Initial release