from stitch_generator.design_utilities.cli import write_pattern_to_file
from stitch_generator.design_utilities.design_collection import designs


def export_all_designs():
    for d in designs:
        write_pattern_to_file(design=d(), parameters={})


if __name__ == "__main__":
    export_all_designs()
