# /// script
# requires-python = ">=3.9"
# dependencies = ["pillow"]
# ///
"""Make a lighter copy of a photo-textured bundle, ``<name>_light_description.tar.gz``.

A textured scene such as a room is light in geometry and heavy in its
photographs (room 13BC: 54 MB, nearly all PNG textures and GLB copies of
them). The copy keeps the OBJ + MTL meshes and every other file, shrinks
each texture so its longer side is at most ``--max-size`` pixels and
stores it as JPEG, and drops the GLB meshes and the ``*_glb.urdf`` files
that use them. Geometry, texture coordinates, joints and collision
geometry are unchanged.

The copy extracts to ``<name>_light_description/`` with its
``package://`` URIs rewritten, so it can sit next to the original.

    uv run tools/make_light_textures.py room13bc_description.tar.gz
"""

import argparse
import glob
import gzip
import io
import os
import re
import shutil
import tarfile
import tempfile


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


def shrink_texture(path, max_size, quality):
    """Rewrite the image at ``path`` as a JPEG no larger than ``max_size``.

    Returns
    -------
    str
        The new file's name.
    """
    from PIL import Image

    with Image.open(path) as image:
        image = image.convert('RGB')
        scale = float(max_size) / max(image.size)
        if scale < 1.0:
            image = image.resize(
                (max(1, round(image.width * scale)),
                 max(1, round(image.height * scale))),
                Image.LANCZOS)
        buf = io.BytesIO()
        # No EXIF or timestamps: the same input gives the same bytes.
        image.save(buf, 'JPEG', quality=quality, optimize=True)
    os.remove(path)
    out = os.path.splitext(path)[0] + '.jpg'
    with open(out, 'wb') as f:
        f.write(buf.getvalue())
    return os.path.basename(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('bundle', help='<name>_description.tar.gz')
    parser.add_argument('--max-size', type=int, default=1024,
                        help='longest texture side [px] (default 1024)')
    parser.add_argument('--quality', type=int, default=85,
                        help='JPEG quality (default 85)')
    args = parser.parse_args()

    name = os.path.basename(args.bundle)[:-len('.tar.gz')]
    if not name.endswith('_description'):
        parser.error('expected <name>_description.tar.gz')
    light = name[:-len('_description')] + '_light_description'
    work = tempfile.mkdtemp()
    try:
        with tarfile.open(args.bundle) as tar:
            tar.extractall(work, filter='data')
        root = os.path.join(work, light)
        os.rename(os.path.join(work, name), root)
        for path in glob.glob(os.path.join(work, '**', '._*'), recursive=True):
            os.remove(path)
        for path in glob.glob(os.path.join(root, '**', '*.glb'),
                              recursive=True):
            os.remove(path)
        for path in glob.glob(os.path.join(root, '**', '*_glb.urdf'),
                              recursive=True):
            os.remove(path)
        for path in glob.glob(os.path.join(root, '**', '*.urdf'),
                              recursive=True):
            rewrite(path, 'package://{}/'.format(name),
                    'package://{}/'.format(light))
        for path in glob.glob(os.path.join(root, '**', '*'), recursive=True):
            if path.endswith('.urdf'):
                continue
            if os.path.isfile(path) and os.path.basename(path) in (
                    'package.xml', 'CMakeLists.txt', 'setup.py') \
                    or path.endswith('.launch.py'):
                rewrite(path, name, light)
        before = after = 0
        for mtl in sorted(glob.glob(os.path.join(root, '**', '*.mtl'),
                                    recursive=True)):
            with open(mtl) as f:
                text = f.read()
            directory = os.path.dirname(mtl)
            renamed = {}
            for texture in sorted(set(re.findall(
                    r'^\s*map_Kd\s+(\S+)\s*$', text, flags=re.MULTILINE))):
                path = os.path.join(directory, texture)
                if not os.path.exists(path):
                    # Shared with another MTL and already converted.
                    jpg = os.path.splitext(texture)[0] + '.jpg'
                    if not os.path.exists(os.path.join(directory, jpg)):
                        raise FileNotFoundError(path)
                    renamed[texture] = jpg
                    continue
                before += os.path.getsize(path)
                renamed[texture] = shrink_texture(path, args.max_size,
                                                  args.quality)
                after += os.path.getsize(os.path.join(directory,
                                                      renamed[texture]))
            for old, new in renamed.items():
                text = re.sub(r'(^\s*map_Kd\s+){}\s*$'.format(re.escape(old)),
                              r'\g<1>' + new, text, flags=re.MULTILINE)
            with open(mtl, 'w') as f:
                f.write(text)
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
        print('{}: textures {:.1f} MB -> {:.1f} MB, wrote {} ({:.1f} MB)'.format(
            name, before / 1e6, after / 1e6, out, os.path.getsize(out) / 1e6))
    finally:
        shutil.rmtree(work)


if __name__ == '__main__':
    main()
