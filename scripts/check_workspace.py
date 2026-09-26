#!/usr/bin/env python3
"""Validate the development contract without Java, downloads or game startup."""

import hashlib
import json
from pathlib import Path
import re
import sys
import tomllib

from check_pack import check as check_pack

ROOT = Path(__file__).resolve().parents[1]


def properties(path):
    return dict(line.strip().split('=', 1) for line in path.read_text().splitlines()
                if '=' in line and not line.lstrip().startswith('#'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check():
    props = properties(ROOT / 'gradle.properties')
    pack = tomllib.loads((ROOT / 'pack/pack.toml').read_text())
    require(pack['versions']['minecraft'] == props['minecraft_version'], 'MC versions differ')
    require(pack['versions']['neoforge'] == props['neo_version'], 'NeoForge versions differ')
    require(props['minecraft_version'] == '1.21.1', 'Update the platform specification before changing MC')
    require(re.fullmatch(r'[a-z][a-z0-9_]{1,63}', props['mod_id']), 'Invalid mod id')

    template = (ROOT / 'mods/core/src/main/resources/META-INF/neoforge.mods.toml').read_text()
    expanded = re.sub(r'\$\{(\w+)\}', lambda match: props[match[1]], template)
    metadata = tomllib.loads(expanded)
    require(metadata['mods'][0]['modId'] == props['mod_id'], 'Mod id differs in metadata')
    require(metadata['mods'][0]['version'] == props['mod_version'], 'Mod version differs')
    entrypoint = ROOT / 'mods/core/src/main/java/io/github/patchouliys/endoflight/EndOfLight.java'
    require(f'MOD_ID = "{props["mod_id"]}"' in entrypoint.read_text(), 'Entrypoint mod id differs')

    for java_file in (ROOT / 'mods').rglob('*.java'):
        if 'build' in java_file.parts or 'client' in java_file.relative_to(ROOT / 'mods').parts:
            continue
        require('net.minecraft.client' not in java_file.read_text(),
                f'Client reference in shared code: {java_file.relative_to(ROOT)}')

    for resource in (ROOT / 'mods/core/src').rglob('*.json'):
        json.loads(resource.read_text())

    package = json.loads((ROOT / 'package.json').read_text())
    lock = json.loads((ROOT / 'package-lock.json').read_text())
    require(package['devDependencies'] == lock['packages']['']['devDependencies'], 'npm lock mismatch')
    wrapper = properties(ROOT / 'gradle/wrapper/gradle-wrapper.properties')
    require(re.fullmatch('[0-9a-f]{64}', wrapper.get('distributionSha256Sum', '')),
            'Gradle distribution needs a SHA-256 checksum')
    wrapper_hash = (ROOT / 'gradle/wrapper/gradle-wrapper.jar.sha256').read_text().strip()
    actual_hash = hashlib.sha256((ROOT / 'gradle/wrapper/gradle-wrapper.jar').read_bytes()).hexdigest()
    require(actual_hash == wrapper_hash, 'Gradle wrapper JAR checksum mismatch')
    check_pack()
    print('Workspace static checks OK (compilation and runtime are separate)')


if __name__ == '__main__':
    try:
        check()
    except (KeyError, ValueError, OSError) as error:
        print(f'Workspace check failed: {error}', file=sys.stderr)
        sys.exit(1)
