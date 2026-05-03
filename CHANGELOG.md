# Changelog

## 1.0.0

### Breaking changes

- `Path` no longer exposes member methods such as `split`, `inverse`, `apply_modifier`, `length`, and `is_circular`.
- `Path(...)` now requires explicit `width` and `stroke_alignment` arguments (default values were removed).
- Several function modifiers were renamed (see table below).

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