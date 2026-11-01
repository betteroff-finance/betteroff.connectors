"""Check that the tool catalog check catches stray names, stale docs, and live API drift."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools_catalog import ROOT, check, check_live, render


class ToolCatalogTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        for name in ('plugins', 'skills', 'docs', 'integrations'):
            shutil.copytree(ROOT / name, self.root / name)
        for name in ('README.md', 'AGENTS.md', 'tools.json'):
            shutil.copyfile(ROOT / name, self.root / name)

    def test_repository_passes(self):
        self.assertEqual(check(self.root), [])

    def test_unknown_tool_and_stale_reference_fail(self):
        guide = self.root / 'docs/connector.md'
        guide.write_text(guide.read_text() + '\nCall `betteroff_move_money`.\n')
        catalog = json.loads((self.root / 'tools.json').read_text())
        catalog['tools'][0]['summary'] = 'Changed.'
        (self.root / 'tools.json').write_text(json.dumps(catalog))
        errors = '\n'.join(check(self.root))
        self.assertIn('docs/connector.md: unknown tool betteroff_move_money', errors)
        self.assertIn('docs/tools.md is stale', errors)

    def test_live_scope_drift_fails(self):
        catalog = json.loads((self.root / 'tools.json').read_text())
        tool = catalog['tools'][0]
        operation = {'operationId': tool['name'], 'summary': tool['title'],
                     'security': [{'agentOAuth': ['accounts:read']}]}
        spec = {'info': {'version': catalog['serverVersion'] + '+abc'},
                'paths': {f"/v1/tools/{tool['name']}": {'post': operation},
                          '/v1/tools/old_alias': {'post': {'operationId': 'old_alias', 'deprecated': True}}}}
        (self.root / 'spec.json').write_text(json.dumps(spec))
        errors = '\n'.join(check_live(self.root, (self.root / 'spec.json').as_uri()))
        self.assertIn(f"{tool['name']}: readOnly", errors)
        self.assertIn(f"{tool['name']}: scopes", errors)
        self.assertIn(f"{catalog['tools'][1]['name']}: missing from the API", errors)
        self.assertNotIn('old_alias', errors)

    def test_live_annotations_and_catalog_url(self):
        catalog = json.loads((self.root / 'tools.json').read_text())
        spec = {'info': {'version': catalog['serverVersion']}, 'paths': {
            f"/v1/tools/{tool['name']}": {'post': {
                'operationId': tool['name'], 'summary': tool['title'], 'description': tool['description'],
                'security': [{'agentOAuth': tool['scopes']}],
                'x-mcp-annotations': {'readOnlyHint': tool['readOnly'], 'destructiveHint': tool['destructive']},
            }} for tool in catalog['tools']}}
        target = self.root / 'spec.json'
        catalog['openapi'] = target.as_uri()
        (self.root / 'tools.json').write_text(json.dumps(catalog))
        target.write_text(json.dumps(spec))
        self.assertEqual(check_live(self.root), [])
        for read_only in (True, False):
            tool = next(t for t in catalog['tools'] if t['readOnly'] is read_only)
            operation = spec['paths'][f"/v1/tools/{tool['name']}"]['post']
            for annotation in ({'readOnlyHint': not read_only}, {}, {'readOnlyHint': int(read_only)}):
                with self.subTest(read_only=read_only, annotation=annotation):
                    operation['x-mcp-annotations'] = {'destructiveHint': tool['destructive'], **annotation}
                    target.write_text(json.dumps(spec))
                    errors = check_live(self.root)
                    self.assertEqual(len(errors), 1)
                    self.assertIn(f"{tool['name']}: readOnly", errors[0])
            operation['x-mcp-annotations'] = {'readOnlyHint': read_only, 'destructiveHint': tool['destructive']}

    def test_live_description_destructive_and_count_drift_fail(self):
        catalog = json.loads((self.root / 'tools.json').read_text())
        spec = {'info': {'version': catalog['serverVersion']}, 'paths': {
            f"/v1/tools/{tool['name']}": {'post': {
                'operationId': tool['name'], 'summary': tool['title'], 'description': tool['description'],
                'security': [{'agentOAuth': tool['scopes']}],
                'x-mcp-annotations': {'readOnlyHint': tool['readOnly'], 'destructiveHint': tool['destructive']},
            }} for tool in catalog['tools']}}
        first, second = catalog['tools'][0]['name'], catalog['tools'][1]['name']
        spec['paths'][f'/v1/tools/{first}']['post']['description'] = 'Changed on the server.'
        spec['paths'][f'/v1/tools/{second}']['post']['x-mcp-annotations']['destructiveHint'] = True
        spec['paths']['/v1/tools/betteroff_new_tool'] = {'post': {'operationId': 'betteroff_new_tool'}}
        target = self.root / 'spec.json'
        target.write_text(json.dumps(spec))
        errors = '\n'.join(check_live(self.root, target.as_uri()))
        self.assertIn(f'{first}: description differs from the API', errors)
        self.assertIn(f'{second}: destructive False != API destructiveHint True', errors)
        self.assertIn(f"count: API lists {len(catalog['tools']) + 1} tools, tools.json lists {len(catalog['tools'])}", errors)
        self.assertIn('betteroff_new_tool: missing from tools.json', errors)

    def test_only_cancellation_is_destructive(self):
        catalog = json.loads((ROOT / 'tools.json').read_text())
        self.assertEqual([t['name'] for t in catalog['tools'] if t['destructive']], ['betteroff_cancel_action_request'])
        self.assertTrue(all(t['description'] for t in catalog['tools']))

    def test_live_version_tracks_server_independently_of_package(self):
        catalog = json.loads((self.root / 'tools.json').read_text())
        catalog['version'] = '9.0.0'
        (self.root / 'tools.json').write_text(json.dumps(catalog))
        spec = {'info': {'version': catalog['serverVersion']}, 'paths': {}}
        target = self.root / 'spec.json'
        target.write_text(json.dumps(spec))
        self.assertFalse(any(error.startswith('version:') for error in check_live(self.root, target.as_uri())))
        spec['info']['version'] = '99.0.0'
        target.write_text(json.dumps(spec))
        self.assertTrue(any(error.startswith('version:') for error in check_live(self.root, target.as_uri())))

    def test_readme_tool_count_must_match_exactly(self):
        readme = self.root / 'README.md'
        count = len(json.loads((self.root / 'tools.json').read_text())['tools'])
        readme.write_text(readme.read_text().replace(f'{count} tools', f'1{count} tools'))
        self.assertIn(f'README.md must state "{count} tools"', check(self.root))

    def test_render_counts_tools(self):
        self.assertIn('31 tools: 23 read tools and 8 write tools', render(json.loads((ROOT / 'tools.json').read_text())))


if __name__ == '__main__':
    unittest.main()
