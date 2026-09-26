import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_workspace import ROOT, check_modules, discover_modules, properties
from mod_fixtures import create_module


class MultiModChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.beta = create_module(self.root, 'beta')
        self.alpha = create_module(self.root, 'alpha')
        self.platform = properties(ROOT / 'gradle.properties')

    def change_beta(self, **values):
        path = self.beta / 'mod.json'
        manifest = json.loads(path.read_text())
        manifest.update(values)
        path.write_text(json.dumps(manifest), encoding='utf-8')

    def test_two_modules_and_sorted_ci_matrix(self):
        self.assertEqual(list(check_modules(self.root, self.platform)), ['alpha', 'beta'])

    def test_independent_version_and_escaped_display_text(self):
        original = (self.alpha / 'mod.json').read_bytes()
        self.change_beta(mod_version='2.0.0', mod_name='Quoted "name"',
                         mod_description='Line one\nLine two \\ path \U0001f31f')
        modules = check_modules(self.root, self.platform)
        self.assertEqual(modules['beta']['mod_version'], '2.0.0')
        self.assertEqual((self.alpha / 'mod.json').read_bytes(), original)

    def test_duplicate_mod_id_is_rejected(self):
        self.change_beta(mod_id='fixture_alpha')
        with self.assertRaisesRegex(ValueError, 'beta: duplicate mod_id.*alpha'):
            discover_modules(self.root)

    def test_duplicate_entrypoint_is_rejected(self):
        self.change_beta(mod_group_id='example.alpha', mod_entrypoint='example.alpha.FixtureMod')
        with self.assertRaisesRegex(ValueError, 'beta: duplicate mod_entrypoint.*alpha'):
            discover_modules(self.root)

    def test_incomplete_module_is_not_silently_skipped(self):
        (self.beta / 'mod.json').unlink()
        with self.assertRaisesRegex(ValueError, 'beta: missing mod.json'):
            discover_modules(self.root)

    def test_missing_build_script_is_rejected(self):
        (self.beta / 'build.gradle').unlink()
        with self.assertRaisesRegex(ValueError, 'beta: missing build.gradle'):
            discover_modules(self.root)

    def test_invalid_json_in_second_module_is_rejected(self):
        (self.beta / 'src/main/resources/data/fixture_beta/fixture.json').write_text('{broken')
        with self.assertRaisesRegex(ValueError, 'beta:.*fixture.json'):
            check_modules(self.root, self.platform)

    def test_shared_client_reference_in_second_module_is_rejected(self):
        source = self.beta / 'src/main/java/example/beta/FixtureMod.java'
        source.write_text(source.read_text().replace('import net.neoforged',
                          'import net.minecraft.client.Minecraft;\nimport net.neoforged'))
        with self.assertRaisesRegex(ValueError, 'beta: Client reference'):
            check_modules(self.root, self.platform)

    def test_entrypoint_id_mismatch_is_rejected(self):
        self.change_beta(mod_id='fixture_other')
        with self.assertRaisesRegex(ValueError, 'beta: Entrypoint MOD_ID differs'):
            check_modules(self.root, self.platform)

    def test_unsafe_module_name_is_rejected(self):
        self.beta.rename(self.root / 'mods' / 'bad name')
        with self.assertRaisesRegex(ValueError, 'Invalid module directory'):
            discover_modules(self.root)

    def test_invalid_manifest_type_and_platform_override_are_rejected(self):
        for field, value in [('mod_name', []), ('minecraft_version', 'other')]:
            original = (self.beta / 'mod.json').read_bytes()
            with self.subTest(field=field):
                self.change_beta(**{field: value})
                with self.assertRaisesRegex(ValueError, 'beta: mod.json'):
                    discover_modules(self.root)
            (self.beta / 'mod.json').write_bytes(original)

    def test_empty_workspace_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'mods').mkdir()
            with self.assertRaisesRegex(ValueError, 'At least one module'):
                discover_modules(root)


if __name__ == '__main__':
    unittest.main()
