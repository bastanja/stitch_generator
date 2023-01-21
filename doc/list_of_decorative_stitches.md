# List of Decorative Stitches

| Name                                            | Example                                                                                                               |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------|
| [Alternating Triangles](#alternating-triangles) | ![](images/small_decorative_stitch_alternating_triangles.svg)                                                         |
| [Arrow Chain](#arrow-chain)                     | ![](images/small_decorative_stitch_arrow_chain.svg)                                                                   |
| [Chevron Stitch](#chevron-stitch)               | ![](images/small_decorative_stitch_chevron_stitch.svg)                                                                |
| [Cretan Stitch](#cretan-stitch)                 | ![](images/small_decorative_stitch_cretan_stitch_1.svg) <br/> ![](images/small_decorative_stitch_cretan_stitch_2.svg) |
| [E-Stitch](#e-stitch)                           | ![](images/small_decorative_stitch_e_stitch_1.svg) <br/> ![](images/small_decorative_stitch_e_stitch_2.svg)           |
| [Feather Stitch](#feather-stitch)               | ![](images/small_decorative_stitch_feather_stitch.svg)                                                                |
| [Overlock Stitch](#overlock-stitch)             | ![](images/small_decorative_stitch_overlock_stitch.svg)                                                               |
| [Rhomb Motif Stitch](#rhomb-motif-stitch)       | ![](images/small_decorative_stitch_rhomb_motif_stitch.svg)                                                            |
| [Stem Stitch](#stem-stitch)                     | ![](images/small_decorative_stitch_stem_stitch_1.svg) <br/> ![](images/small_decorative_stitch_stem_stitch_2.svg)     |
| [Three Arrows](#three-arrows)                   | ![](images/small_decorative_stitch_three_arrows.svg)                                                                  |
| [X-Motif Stitch](#x-motif-stitch)               | ![](images/small_decorative_stitch_x_motif_stitch.svg)                                                                |

## Alternating Triangles

Example:

```python
from stitch_generator.collection.stitch_effects.decorative_stitches import alternating_triangles

effect = alternating_triangles(spacing=3, line_length=4, width=5, repetitions=3)
stitches = effect(path)
```

![Decorative Stitch Alternating Triangles](images/decorative_stitch_alternating_triangles.svg)

## Arrow Chain

Example:

```python
from stitch_generator.collection.stitch_effects.decorative_stitches import arrow_chain

effect = arrow_chain(arrow_width=5, arrow_length=2, arrow_spacing=3)
stitches = effect(path)
```

![Decorative Stitch Arrow Chain](images/decorative_stitch_arrow_chain.svg)

## Chevron Stitch

Example:

```python
from stitch_generator.collection.stitch_effects.decorative_stitches import chevron_stitch

effect = chevron_stitch(spacing=6, line_length=3, width=5, repetitions=5)
stitches = effect(path)
```

![Decorative Stitch Chevron Stitch](images/decorative_stitch_chevron_stitch.svg)

## Cretan Stitch

Example:

```python
from stitch_generator.collection.stitch_effects.decorative_stitches import cretan_stitch

effect = cretan_stitch(spacing=6, stitch_width=0.1, stitch_length=3, repetitions=4, zigzag_width=2)
stitches = effect(path)
```

![Decorative Stitch Cretan Stitch 1](images/decorative_stitch_cretan_stitch_1.svg)

Example:

```python
from stitch_generator.collection.stitch_effects.decorative_stitches import cretan_stitch

effect = cretan_stitch(spacing=6, stitch_width=0.1, stitch_length=3.5, repetitions=4)
stitches = effect(path)
```

![Decorative Stitch Cretan Stitch 2](images/decorative_stitch_cretan_stitch_2.svg)

## E-Stitch

Example:

```python
from stitch_generator.collection.stitch_effects.decorative_stitches import e_stitch

effect = e_stitch(spacing=3, line_length=4, stitch_length=10, angle=0)
stitches = effect(path)
```

![Decorative Stitch E-Stitch 1](images/decorative_stitch_e_stitch_1.svg)

Example:

```python
from stitch_generator.collection.stitch_effects.decorative_stitches import e_stitch

effect = e_stitch(spacing=3, line_length=4, stitch_length=10, angle=45)
stitches = effect(path)
```

![Decorative Stitch E-Stitch 2](images/decorative_stitch_e_stitch_2.svg)

## Feather Stitch

Example:

```python
from stitch_generator.collection.stitch_effects.decorative_stitches import feather_stitch

effect = feather_stitch(spacing=3, stitch_width=0, stitch_length=3.5, repetitions=2)
stitches = effect(path)
```

![Decorative Stitch Feather Stitch](images/decorative_stitch_feather_stitch.svg)

## Overlock Stitch

Example:

```python
from stitch_generator.collection.stitch_effects.decorative_stitches import overlock_stitch

effect = overlock_stitch(length=3, width=5)
stitches = effect(path)
```

![Decorative Stitch Overlock Stitch](images/decorative_stitch_overlock_stitch.svg)

## Rhomb Motif Stitch

Example:

```python
from stitch_generator.collection.stitch_effects.decorative_stitches import rhomb_motif_stitch

effect = rhomb_motif_stitch(spacing=3, width=6, length=5)
stitches = effect(path)
```

![Decorative Stitch Rhomb Motif Stitch](images/decorative_stitch_rhomb_motif_stitch.svg)

## Stem Stitch

Example:

```python
from stitch_generator.collection.stitch_effects.decorative_stitches import stem_stitch

effect = stem_stitch(spacing=3, stitch_width=0.6, stitch_length=5, repetitions=5, angle=25)
stitches = effect(path)
```

![Decorative Stitch Stem Stitch 1](images/decorative_stitch_stem_stitch_1.svg)

Example:

```python
from stitch_generator.collection.stitch_effects.decorative_stitches import stem_stitch

effect = stem_stitch(spacing=3, stitch_width=5, stitch_length=4, repetitions=5, angle=0)
stitches = effect(path)
```

![Decorative Stitch Stem Stitch 2](images/decorative_stitch_stem_stitch_2.svg)

## Three Arrows

Example:

```python
from stitch_generator.collection.stitch_effects.decorative_stitches import three_arrows

effect = three_arrows(arrow_spacing=2, group_spacing=20, start_end_spacing=10, stitch_length=3)
stitches = effect(path)
```

![Decorative Stitch Three Arrows](images/decorative_stitch_three_arrows.svg)

## X Motif Stitch

Example:

```python
from stitch_generator.collection.stitch_effects.decorative_stitches import x_motif_stitch

effect = x_motif_stitch(spacing=3, width=6, length=5)
stitches = effect(path)
```

![Decorative Stitch X Motif Stitch](images/decorative_stitch_x_motif_stitch.svg)
