"""Temporary independent mods for workspace and build regression tests."""

import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def create_module(root, name):
    directory = root / 'mods' / name
    directory.mkdir(parents=True)
    shutil.copyfile(ROOT / 'mods/core/build.gradle', directory / 'build.gradle')
    metadata = directory / 'src/main/resources/META-INF/neoforge.mods.toml'
    metadata.parent.mkdir(parents=True)
    shutil.copyfile(ROOT / 'mods/core/src/main/resources/META-INF/neoforge.mods.toml', metadata)
    manifest = {
        'mod_id': f'fixture_{name}', 'mod_name': f'Fixture {name}', 'mod_version': '0.2.0',
        'mod_group_id': f'example.{name}', 'mod_license': 'All Rights Reserved',
        'mod_authors': 'Example', 'mod_description': f'Independent {name} fixture.',
        'mod_entrypoint': f'example.{name}.FixtureMod',
    }
    (directory / 'mod.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    source = directory / f'src/main/java/example/{name}/FixtureMod.java'
    source.parent.mkdir(parents=True)
    source.write_text(f'''package example.{name};

import net.neoforged.fml.common.Mod;

@Mod(FixtureMod.MOD_ID)
public final class FixtureMod {{
    public static final String MOD_ID = "fixture_{name}";
}}
''', encoding='utf-8')
    resource = directory / f'src/main/resources/data/fixture_{name}/fixture.json'
    resource.parent.mkdir(parents=True)
    resource.write_text(json.dumps({'module': name}), encoding='utf-8')
    return directory
