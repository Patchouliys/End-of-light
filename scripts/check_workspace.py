#!/usr/bin/env python3
"""Validate the development contract without Java, downloads or game startup."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import tomllib

from check_pack import check as check_pack

ROOT = Path(__file__).resolve().parents[1]
MOD_FIELDS = {'mod_id', 'mod_name', 'mod_version', 'mod_group_id', 'mod_license',
              'mod_authors', 'mod_description', 'mod_entrypoint'}
TEXT_FIELDS = ('mod_name', 'mod_license', 'mod_authors', 'mod_description')


def properties(path):
    return dict(line.strip().split('=', 1) for line in path.read_text().splitlines()
                if '=' in line and not line.lstrip().startswith('#'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def discover_modules(root=ROOT):
    modules = {}
    identities = {'mod_id': {}, 'mod_entrypoint': {}}
    for directory in sorted((root / 'mods').iterdir()):
        if directory.name.startswith('.') or not directory.is_dir():
            continue
        name = directory.name
        require(not directory.is_symlink(), f'{name}: module directories cannot be symlinks')
        require(re.fullmatch(r'[a-z][a-z0-9_-]*', name), f'Invalid module directory: {name}')
        for filename in ('build.gradle', 'mod.json'):
            require((directory / filename).is_file(), f'{name}: missing {filename}')
        try:
            manifest = json.loads((directory / 'mod.json').read_text(encoding='utf-8'))
        except ValueError as error:
            raise ValueError(f'{name}/mod.json: {error}') from error
        require(isinstance(manifest, dict), f'{name}: mod.json must be an object')
        require(set(manifest) == MOD_FIELDS, f'{name}: mod.json must contain {sorted(MOD_FIELDS)}')
        require(all(isinstance(v, str) and v.strip() for v in manifest.values()),
                f'{name}: mod.json values must be nonempty strings')
        require(re.fullmatch(r'[a-z][a-z0-9_]{1,63}', manifest['mod_id']), f'{name}: invalid Mod ID')
        require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9.+_-]*', manifest['mod_version']),
                f'{name}: invalid mod version')
        for field in ('mod_group_id', 'mod_entrypoint'):
            require(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)+', manifest[field]),
                    f'{name}: invalid {field}')
        require(manifest['mod_entrypoint'].startswith(manifest['mod_group_id'] + '.'),
                f'{name}: entry point must be inside its package prefix')
        for field, seen in identities.items():
            value = manifest[field]
            require(value not in seen, f'{name}: duplicate {field} {value} with {seen.get(value)}')
            seen[value] = name
        modules[name] = manifest
    require(modules, 'At least one module is required under mods/')
    return modules


def check_module(directory, manifest, platform):
    values = dict(manifest, minecraft_version=platform['minecraft_version'], neo_version=platform['neo_version'])
    values.update({f'{key}_toml': json.dumps(manifest[key], ensure_ascii=False) for key in TEXT_FIELDS})
    template = (directory / 'src/main/resources/META-INF/neoforge.mods.toml').read_text(encoding='utf-8')
    expanded = re.sub(r'\$\{(\w+)\}', lambda match: values[match[1]], template)
    metadata = tomllib.loads(expanded)
    require(len(metadata['mods']) == 1, 'Each module must declare exactly one mod')
    mod = metadata['mods'][0]
    for field, key in [('modId', 'mod_id'), ('version', 'mod_version'), ('displayName', 'mod_name'),
                       ('authors', 'mod_authors'), ('description', 'mod_description')]:
        require(mod[field] == manifest[key], f'Metadata {field} differs from mod.json')
    require(metadata['license'] == manifest['mod_license'], 'Metadata license differs')
    dependencies = {entry['modId']: entry for entry in metadata['dependencies'][manifest['mod_id']]}
    for dependency, version in [('minecraft', platform['minecraft_version']), ('neoforge', platform['neo_version'])]:
        require(dependencies[dependency]['versionRange'] == f'[{version}]', f'{dependency} version differs')
        require(dependencies[dependency]['type'] == 'required', f'{dependency} must be required')

    source = directory / 'src/main/java' / (manifest['mod_entrypoint'].replace('.', '/') + '.java')
    text = source.read_text(encoding='utf-8')
    require(re.search(r'\bMOD_ID\s*=\s*"' + re.escape(manifest['mod_id']) + '"', text),
            'Entrypoint MOD_ID differs from mod.json')
    package = manifest['mod_entrypoint'].rsplit('.', 1)[0]
    require(re.search(r'\bpackage\s+' + re.escape(package) + r'\s*;', text), 'Entrypoint package differs')

    for java_file in (directory / 'src').rglob('*.java'):
        if 'client' not in java_file.relative_to(directory / 'src').parts:
            require('net.minecraft.client' not in java_file.read_text(encoding='utf-8'),
                    f'Client reference in shared code: {java_file.relative_to(directory)}')
    for resource in (directory / 'src').rglob('*.json'):
        try:
            json.loads(resource.read_text(encoding='utf-8'))
        except ValueError as error:
            raise ValueError(f'{resource.relative_to(directory)}: {error}') from error


def check_modules(root, platform):
    modules = discover_modules(root)
    for name, manifest in modules.items():
        try:
            check_module(root / 'mods' / name, manifest, platform)
        except (KeyError, ValueError, OSError, TypeError, IndexError) as error:
            raise ValueError(f'{name}: {error}') from error
    return modules


def check():
    props = properties(ROOT / 'gradle.properties')
    pack = tomllib.loads((ROOT / 'pack/pack.toml').read_text())
    require(pack['versions']['minecraft'] == props['minecraft_version'], 'MC versions differ')
    require(pack['versions']['neoforge'] == props['neo_version'], 'NeoForge versions differ')
    require(props['minecraft_version'] == '1.21.1', 'Update the platform specification before changing MC')
    require(not (set(props) & MOD_FIELDS), 'Mod identity belongs in each module mod.json')
    modules = check_modules(ROOT, props)

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
    print(f'Workspace static checks OK: {len(modules)} module(s) (compilation and runtime are separate)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list-modules', action='store_true', help='Print validated module names as a JSON array')
    args = parser.parse_args()
    try:
        if args.list_modules:
            print(json.dumps(list(discover_modules())))
        else:
            check()
    except (KeyError, ValueError, OSError) as error:
        print(f'Workspace check failed: {error}', file=sys.stderr)
        sys.exit(1)
