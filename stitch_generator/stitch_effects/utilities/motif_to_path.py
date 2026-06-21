from stitch_generator.framework import Array2D, Path


def motif_to_path(motif: Array2D, path: Path):
    tx = motif[:, 0]
    ty = motif[:, 1]
    return (
        path.shape(tx).T
        + path.direction(tx).T * path.width(tx) * (path.stroke_alignment(tx) - ty)
    ).T
