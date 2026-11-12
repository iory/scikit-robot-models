# /// script
# requires-python = ">=3.9"
# dependencies = ["scikit-robot>=0.4.15", "DracoPy", "numpy", "trimesh"]
# ///
"""Make a Draco copy of a bundle, ``<robot>_draco_description.tar.gz``.

Every mesh the URDFs reference is rewritten as a GLB with
KHR_draco_mesh_compression, through scikit-robot's own GLB writer, so the
faces stay as they are and only the encoding shrinks (positions quantised
to 14 bits). Colours are kept as vertex colours. Nothing else in the URDFs
changes but the mesh file names (``.stl``/``.dae`` become ``.glb``) and the
``package://`` URIs, which point at ``<robot>_draco_description/`` so the
copy can sit next to the original.

Loading it needs DracoPy. Gazebo and RViz cannot decode Draco meshes; keep
the uncompressed bundle for them.

    uv run tools/make_draco.py jedy_description.tar.gz
    uv run tools/make_draco.py path/to/jedy_description/
"""

import argparse
import glob
import gzip
import os
import re
import shutil
import tarfile
import tempfile

from make_light import clean
from make_light import rewrite

MESH_URI = re.compile(r'filename="(package://[^"]+\.(?:glb|stl|dae))"',
                      re.IGNORECASE)
COMMENT = re.compile(r'<!--.*?-->', re.DOTALL)


def compress(src, dst):
    """Write the meshes in ``src`` to ``dst`` as a Draco GLB.

    Returns
    -------
    int
        Number of faces written.
    """
    from skrobot.utils import urdf_mesh

    meshes = urdf_mesh.load_meshes(src)
    if not meshes:
        raise RuntimeError('no geometry in {}'.format(src))
    with urdf_mesh.export_mesh_format('glb', draco_compression=True):
        urdf_mesh._write_gltf(meshes, dst)
    return sum(len(m.faces) for m in meshes)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('bundle',
                        help='<robot>_description.tar.gz or its directory')
    args = parser.parse_args()

    bundle = args.bundle.rstrip('/\\')
    name = os.path.basename(bundle)
    if name.endswith('.tar.gz'):
        name = name[:-len('.tar.gz')]
    if not name.endswith('_description'):
        parser.error('expected <robot>_description(.tar.gz)')
    draco = name[:-len('_description')] + '_draco_description'
    work = tempfile.mkdtemp()
    try:
        root = os.path.join(work, draco)
        if os.path.isdir(bundle):
            shutil.copytree(bundle, root)
        else:
            with tarfile.open(bundle) as tar:
                tar.extractall(work, filter='data')
            os.rename(os.path.join(work, name), root)
        for path in glob.glob(os.path.join(work, '**', '._*'), recursive=True):
            os.remove(path)
        package = os.path.join(root, 'package.xml')
        if os.path.exists(package):
            rewrite(package, '<name>{}</name>'.format(name),
                    '<name>{}</name>'.format(draco))

        urdfs = sorted(glob.glob(os.path.join(root, '**', '*.urdf'),
                                 recursive=True))
        prefix = 'package://{}/'.format(name)
        sources = set()
        for path in urdfs:
            with open(path) as f:
                # Commented-out elements may name files that are not there.
                text = COMMENT.sub('', f.read())
                for uri in MESH_URI.findall(text):
                    if not uri.startswith(prefix):
                        raise RuntimeError(
                            '{} is outside {}'.format(uri, name))
                    sources.add(uri[len(prefix):])
        targets = {}
        # Sorted, a GLB comes before an STL of the same name and keeps it;
        # the STL becomes <name>_stl.glb.
        for rel in sorted(sources):
            stem, ext = os.path.splitext(rel)
            out = stem + '.glb'
            if out in targets.values():
                out = '{}_{}.glb'.format(stem, ext[1:].lower())
            if out in targets.values() or (out not in sources
                                           and os.path.exists(
                                               os.path.join(root, out))):
                raise RuntimeError('two meshes would become {}'.format(out))
            targets[rel] = out

        before = sum(os.path.getsize(os.path.join(root, r)) for r in sources)
        faces = 0
        converted = {}
        for rel, out in targets.items():
            tmp = os.path.join(work, 'tmp.glb')
            faces += compress(os.path.join(root, rel), tmp)
            converted[out] = tmp + '.' + str(len(converted))
            os.replace(tmp, converted[out])
        # Only now drop the originals: a .glb source may share its name
        # with another source's output.
        for rel in sources:
            os.remove(os.path.join(root, rel))
        for out, tmp in converted.items():
            os.replace(tmp, os.path.join(root, out))
        after = sum(os.path.getsize(os.path.join(root, o))
                    for o in targets.values())

        for path in urdfs:
            with open(path) as f:
                text = f.read()
            for rel, out in targets.items():
                text = text.replace('"{}{}"'.format(prefix, rel),
                                    '"package://{}/{}"'.format(draco, out))
            # What is left is in comments.
            text = text.replace(prefix, 'package://{}/'.format(draco))
            with open(path, 'w', newline='') as f:
                f.write(text)

        out = draco + '.tar.gz'
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
        print('{}: {} meshes, {} faces, {:.1f} MB -> {:.1f} MB, wrote {}'
              .format(name, len(targets), faces, before / 1e6, after / 1e6,
                      out))
    finally:
        shutil.rmtree(work)


if __name__ == '__main__':
    main()
