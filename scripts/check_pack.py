#!/usr/bin/env python3
"""Read-only checks for packwiz hashes, metadata and paths. Python 3.11+."""

import hashlib
from pathlib import Path, PurePosixPath
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    with path.open('rb') as stream:
        return tomllib.load(stream)


def contained_file(root, name):
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or '\\' in name:
        raise ValueError(f'Unsafe pack path: {name}')
    result = root / name
    if result.is_symlink() or not result.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Pack path leaves root or is a symlink: {name}')
    if not result.is_file():
        raise ValueError(f'Missing pack file: {name}')
    return result


def check_hash(path, algorithm, expected):
    if algorithm not in {'sha256', 'sha512', 'sha1', 'md5'}:
        raise ValueError(f'Unsupported hash algorithm {algorithm}: {path}')
    actual = hashlib.new(algorithm, path.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(f'Stale hash for {path}; run packwiz refresh')


def check(pack_root=ROOT / 'pack'):
    pack = load(pack_root / 'pack.toml')
    index_info = pack['index']
    index_path = contained_file(pack_root, index_info['file'])
    check_hash(index_path, index_info['hash-format'], index_info['hash'])
    index = load(index_path)
    seen = set()
    for entry in index.get('files', []):
        name = entry['file']
        if name in seen:
            raise ValueError(f'Duplicate pack entry: {name}')
        seen.add(name)
        path = contained_file(pack_root, name)
        check_hash(path, entry.get('hash-format', index['hash-format']), entry['hash'])
        if entry.get('metafile'):
            metadata = load(path)
            if metadata.get('side', 'both') not in {'client', 'server', 'both'}:
                raise ValueError(f'Invalid side: {name}')
            filename = metadata['filename']
            if '/' in filename or '\\' in filename or filename in {'', '.', '..'}:
                raise ValueError(f'Invalid downloaded filename: {name}')
            download = metadata['download']
            algorithm = download['hash-format']
            digest = download['hash']
            sizes = {'sha256': 64, 'sha512': 128, 'sha1': 40, 'md5': 32}
            if algorithm in sizes and (len(digest) != sizes[algorithm] or
                    any(c not in '0123456789abcdef' for c in digest.lower())):
                raise ValueError(f'Invalid download hash: {name}')
            if algorithm not in {*sizes, 'murmur2'}:
                raise ValueError(f'Unknown download hash: {name}')
    print(f'packwiz index OK: {len(seen)} entries (no game launched)')


if __name__ == '__main__':
    try:
        check()
    except (KeyError, ValueError, OSError) as error:
        print(f'Pack check failed: {error}', file=sys.stderr)
        sys.exit(1)
