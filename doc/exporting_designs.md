# Install stitch_generator

Make sure to have a python3 environment and pip available. Clone the stitch_generator repository.
From the stitch_generator folder, install the requirements and stitch_generator:

    pip install -r requirements.txt
    pip install .

# Export an existing design

The sample designs are in folder [stitch_generator/designs](../stitch_generator/designs). To export
a design, call the script of the design and pass the desired export format as argument:

    python stitch_generator/designs/noise_spiral.py --format=svg

You can find the result in the current folder, e.g. as noise_spiral.svg

Most designs have multiple parameters you can pass as arguments to the export call. To see all
parameters, call the design script with --help:

    python stitch_generator/designs/noise_spiral.py --help

This will write the names of all parameters, their default value and their allowed value range.

Example for changing the inner_radius parameter of the design noise_spiral:

    python stitch_generator/designs/noise_spiral.py --format=svg --inner_radius=50

# Create and export a new design

To create an own design, copy the design template:

    cp stitch_generator/design_utilities/template.py my_design.py

Edit my_design.py:

- Change the name `name="template_design"` to the name of your design. This will be the file name of
  the exported files.
- Change the parameters: The template design has the parameters `stitch_length` and `length`. Add or
  remove parameters as desired. These parameters are available as command line arguments when you
  export the design.
- Implement the `get_pattern` function. In this function you can access the parameters of the design
  and create the stitches for the embroidery design. Read about the
  [basic concepts of stitch_generator](basic_concepts.md) to find out how to create the stitches.

When you are ready with your changes, export the design:

    python my_design.py --format=svg
