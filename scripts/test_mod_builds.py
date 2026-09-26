#!/usr/bin/env python3
"""Verify two temporary NeoForge modules with Java 21, without launching Minecraft."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
from mod_fixtures import create_module


def run_build(root, *tasks, succeeds=True):
    wrapper = 'gradlew.bat' if sys.platform == 'win32' else './gradlew'
    result = subprocess.run([wrapper, '--no-daemon', '--console=plain', *tasks], cwd=root,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if (result.returncode == 0) != succeeds:
        print(result.stdout)
        raise AssertionError(f'Unexpected build result for {tasks}: {result.returncode}')
    return result.stdout


def check_jar(directory, name, manifest):
    jar = directory / f'build/libs/fixture_{name}-{manifest["mod_version"]}.jar'
    other = 'beta' if name == 'alpha' else 'alpha'
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        assert f'example/{name}/FixtureMod.class' in names
        assert f'data/fixture_{name}/fixture.json' in names
        assert not any(f'/{other}/' in n or f'fixture_{other}/' in n for n in names)
        metadata = tomllib.loads(archive.read('META-INF/neoforge.mods.toml').decode())
        mod = metadata['mods'][0]
        assert mod['modId'] == manifest['mod_id']
        assert mod['version'] == manifest['mod_version']
        assert mod['displayName'] == manifest['mod_name']
        assert mod['description'] == manifest['mod_description']
    return jar.read_bytes()


def main():
    with tempfile.TemporaryDirectory(prefix='endoflight-build-') as temp:
        root = Path(temp)
        for name in ('settings.gradle', 'build.gradle', 'gradle.properties', 'gradlew', 'gradlew.bat'):
            shutil.copy2(ROOT / name, root / name)
        shutil.copytree(ROOT / 'gradle', root / 'gradle')
        alpha = create_module(root, 'alpha')
        beta = create_module(root, 'beta')
        beta_manifest = json.loads((beta / 'mod.json').read_text())
        beta_manifest.update(mod_version='1.2.3', mod_name='Beta "quoted"',
                             mod_description='Line one\nLine two \\ path \U0001f31f')
        (beta / 'mod.json').write_text(json.dumps(beta_manifest))
        source = beta / 'src/main/java/example/beta/FixtureMod.java'
        valid_source = source.read_text()
        source.write_text(valid_source + '\ninvalid Java\n')

        print('Building alpha while independent beta has a compile error...', flush=True)
        output = run_build(root, ':alpha:build')
        assert ':beta:compileJava' not in output
        assert not (beta / 'build/libs').exists()
        alpha_manifest = json.loads((alpha / 'mod.json').read_text())
        alpha_jar = check_jar(alpha, 'alpha', alpha_manifest)

        print('Checking aggregate build detects beta failure...', flush=True)
        output = run_build(root, ':build', succeeds=False)
        assert ':beta:compileJava FAILED' in output
        source.write_text(valid_source)

        print('Building both mods and checking separate JARs and metadata...', flush=True)
        run_build(root, ':build')
        assert check_jar(alpha, 'alpha', alpha_manifest) == alpha_jar
        check_jar(beta, 'beta', beta_manifest)

        print('Checking selective clean preserves the other mod...', flush=True)
        run_build(root, ':beta:clean')
        assert not (beta / 'build').exists()
        assert check_jar(alpha, 'alpha', alpha_manifest) == alpha_jar
        run_build(root, ':clean')
        assert not (alpha / 'build').exists()
        print('Multi-mod build regression passed; no game launched.')


if __name__ == '__main__':
    main()
