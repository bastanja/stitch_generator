# Satin
A zig-zag line between the left and right boundary of the Path.

Also supports a variety of satin stitch patterns

The satin stitch effect does not include the underlay. To create an underlay, use the underlay
stitch effect on an underlay Path.

# Meander
A line that meanders back and forth between the left and right boundary of the Path.

# Contour
A running stitch line along the left and right boundary of the Path, closed at both ends.

# Lattice
A continuous line going back and forth between the left and right boundary of the Path. Creates
a grid-like pattern.

# Stripes
A zig-zag line along the Path. Similar to satin, but in the direction of the Path instead of
perpendicular to it

# Scribble
A zig-zag line repeating along the Path with random offsets to the side to simulate a hand-drawn
scribble line. Useful for appliqués.

# Double Satin
A zig-zag line between the left and right boundary of the Path in forward direction and an inverse
zig-zag line back from the end to the start of the Path.

Useful as part of an underlay

# Underlay
A pattern of lines to be used below satin stitches. It raises the satin stitches and gives them a
firm foundation.

To avoid that the underlay sticks out below the satin stitches, the path for the underlay should have a smaller width and be a bit shorter than the path of the Satin stitches. Use `stitch_generator.functions.get_underlay_path` to create such a Path.