import os
import re


def change_imports(directory):
    pattern = re.compile(r"(from stitch_generator(?:\.[^.]+)*)\.([^.]+) import")

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r") as f:
                    lines = f.readlines()

                changed = False
                for i, line in enumerate(lines):
                    if line.strip().startswith("from stitch_generator"):
                        new_line = pattern.sub(r"\1 import", line)
                        if new_line != line:
                            lines[i] = new_line
                            changed = True

                if changed:
                    with open(filepath, "w") as f:
                        f.writelines(lines)
                    print(f"Updated: {filepath}")


if __name__ == "__main__":
    change_imports("stitch_generator")
