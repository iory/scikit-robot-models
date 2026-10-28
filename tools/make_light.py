# /// script
# requires-python = ">=3.9"
# dependencies = ["meshoptimizer", "numpy", "scipy", "trimesh"]
# ///
"""Make a lighter copy of a bundle, ``<robot>_light_description.tar.gz``.

CAD exports carry far more faces than a simulator or a browser needs
(Jedy: about 700,000). The copy drops circuit boards and parts smaller
than ``--min-size`` (screws, connectors), and simplifies every other part
with meshoptimizer as far as it goes without moving its surface more than
``--max-error``: an error bound rather than a face ratio, so thin plates
and gears keep their shape. Each part is coloured with its average colour.

The copy extracts to ``<robot>_light_description/`` with its
``package://`` URIs rewritten, so it can sit next to the original.

    uv run tools/make_light.py jedy_description.tar.gz
"""

import argparse
import glob
import gzip
import os
import shutil
import tarfile
import tempfile

import numpy as np


def is_board(color):
    """Whether an average RGB colour is a circuit board's green or blue."""
    r, g, b = (int(c) for c in color[:3])
    return (g > r + 40 and g > b + 20) or (b > r + 60 and b > 120 and g < 150)


def simplify(mesh, max_error):
    """``mesh`` simplified within ``max_error``, or None if nothing is left."""
    import meshoptimizer
    import trimesh

    welded = mesh.copy()
    # CAD exports split vertices per face for flat shading; unwelded, every
    # triangle is its own border and nothing can be simplified.
    welded.merge_vertices(merge_tex=True, merge_norm=True)
    indices = welded.faces.astype(np.uint32).ravel()
    result = np.zeros_like(indices)
    count = meshoptimizer.simplify(
        result, indices, welded.vertices.astype(np.float32),
        target_index_count=0, target_error=max_error,
        options=(meshoptimizer.SIMPLIFY_ERROR_ABSOLUTE
                 | meshoptimizer.SIMPLIFY_PRUNE))
    if count == 0:
        return None
    reduced = trimesh.Trimesh(welded.vertices, result[:count].reshape(-1, 3),
                              process=False)
    reduced.remove_unreferenced_vertices()
    return reduced


def reduce_mesh_file(path, max_error, min_size):
    """Drop boards and small parts from the GLB at ``path``, simplify the
    rest, in place.

    Returns
    -------
    tuple[int, int]
        Faces before and after.
    """
    import trimesh

    scene = trimesh.load(path)
    before = after = 0
    for name, mesh in list(scene.geometry.items()):
        before += len(mesh.faces)
        color = np.round(np.mean(mesh.visual.vertex_colors, axis=0))
        reduced = None
        if (max(mesh.bounding_box.extents) >= min_size
                and not is_board(color)):
            reduced = simplify(mesh, max_error)
        if reduced is None:
            scene.delete_geometry(name)
            continue
        reduced.visual.face_colors = color.astype(np.uint8)
        # Same units as the original parts, or trimesh warns about mixed
        # units each time the file loads.
        reduced.units = mesh.units
        scene.geometry[name] = reduced
        after += len(reduced.faces)
    scene.export(path)
    return before, after


def rewrite(path, old, new):
    with open(path) as f:
        text = f.read()
    with open(path, 'w') as f:
        f.write(text.replace(old, new))


def clean(info):
    """Tar entry without owner, timestamp or macOS metadata."""
    if os.path.basename(info.name).startswith('._'):
        return None
    info.uid = info.gid = 0
    info.uname = info.gname = ''
    info.mtime = 0
    info.pax_headers = {}
    return info


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('bundle', help='<robot>_description.tar.gz')
    parser.add_argument('--max-error', type=float, default=0.0005,
                        help='largest surface deviation [m] (default 0.5 mm)')
    parser.add_argument('--min-size', type=float, default=0.01,
                        help='parts smaller than this [m] are dropped')
    args = parser.parse_args()

    name = os.path.basename(args.bundle)[:-len('.tar.gz')]
    if not name.endswith('_description'):
        parser.error('expected <robot>_description.tar.gz')
    light = name[:-len('_description')] + '_light_description'
    work = tempfile.mkdtemp()
    try:
        with tarfile.open(args.bundle) as tar:
            tar.extractall(work, filter='data')
        root = os.path.join(work, light)
        os.rename(os.path.join(work, name), root)
        for path in glob.glob(os.path.join(work, '**', '._*'), recursive=True):
            os.remove(path)
        for path in glob.glob(os.path.join(root, '**', '*.urdf'),
                              recursive=True):
            rewrite(path, 'package://{}/'.format(name),
                    'package://{}/'.format(light))
        package = os.path.join(root, 'package.xml')
        if os.path.exists(package):
            rewrite(package, '<name>{}</name>'.format(name),
                    '<name>{}</name>'.format(light))
        before = after = 0
        for path in sorted(glob.glob(os.path.join(root, '**', '*.glb'),
                                     recursive=True)):
            b, a = reduce_mesh_file(path, args.max_error, args.min_size)
            before += b
            after += a
        out = light + '.tar.gz'
        # Fixed order and no timestamps, so the same input gives the same
        # bytes (and md5).
        with gzip.GzipFile(out, 'wb', mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode='w',
                              format=tarfile.GNU_FORMAT) as tar:
                for dirpath, dirnames, filenames in os.walk(root):
                    dirnames.sort()
                    tar.add(dirpath, os.path.relpath(dirpath, work),
                            recursive=False, filter=clean)
                    for filename in sorted(filenames):
                        path = os.path.join(dirpath, filename)
                        tar.add(path, os.path.relpath(path, work),
                                filter=clean)
        print('{}: {} -> {} faces, wrote {}'.format(name, before, after, out))
    finally:
        shutil.rmtree(work)


if __name__ == '__main__':
    main()
