"""Check that the tool catalog check catches stray names, stale docs, and live API drift."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools_catalog import ROOT, check, check_live, render


def live_operation(tool):
    return {'operationId': tool['name'], 'summary': tool['title'], 'description': tool.get('description'),
            'security': [{'agentOAuth': tool['scopes']}],
            'x-mcp-annotations': {'readOnlyHint': tool['readOnly'],
                                  'destructiveHint': tool.get('destructive', False)}}


def live_spec(catalog):
    return {'info': {'version': catalog['serverVersion']}, 'paths': {
        f"/v1/tools/{tool['name']}": {'post': live_operation(tool)}
        for tool in catalog['tools'] if not tool.get('unavailable')}}


class ToolCatalogTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        for name in ('plugins', 'skills', 'docs', 'integrations'):
            shutil.copytree(ROOT / name, self.root / name)
        for name in ('README.md', 'tools.json'):
            shutil.copyfile(ROOT / name, self.root / name)

    def test_unavailable_and_any_scope_tools_render_honestly(self):
        table = render(json.loads((self.root / 'tools.json').read_text()))
        self.assertIn('`transfers:prepare` or `transfers:bank` or `transfers:vault`', table)
        self.assertRegex(table, r'betteroff_request_bank_transfer.*Not available right now\.')

    def test_live_check_expects_no_unavailable_tool(self):
        catalog = json.loads((self.root / 'tools.json').read_text())
        spec = live_spec(catalog)
        for t in catalog['tools']:
            if not t.get('unavailable'):
                spec['paths'][f"/v1/tools/{t['name']}"]['post']['security'] = [{'agentOAuth': [s]} for s in t['scopes']]
        path = self.root / 'spec.json'
        path.write_text(json.dumps(spec))
        self.assertEqual(check_live(self.root, path.as_uri()), [])

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
        spec = live_spec(catalog)
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
                    operation['x-mcp-annotations'] = {'destructiveHint': tool.get('destructive', False), **annotation}
                    target.write_text(json.dumps(spec))
                    errors = check_live(self.root)
                    self.assertEqual(len(errors), 1)
                    self.assertIn(f"{tool['name']}: readOnly", errors[0])
            operation['x-mcp-annotations'] = {'readOnlyHint': read_only,
                                              'destructiveHint': tool.get('destructive', False)}

    def test_only_cancel_action_request_is_destructive(self):
        tools = json.loads((ROOT / 'tools.json').read_text())['tools']
        self.assertEqual([t['name'] for t in tools if t.get('destructive')], ['betteroff_cancel_action_request'])

    def test_live_description_drift_fails(self):
        catalog = json.loads((self.root / 'tools.json').read_text())
        first, second = catalog['tools'][:2]
        spec = live_spec(catalog)
        spec['paths'][f"/v1/tools/{first['name']}"]['post']['description'] = 'Changed on the server.'
        del second['description']
        (self.root / 'tools.json').write_text(json.dumps(catalog))
        (self.root / 'spec.json').write_text(json.dumps(spec))
        self.assertEqual(check_live(self.root, (self.root / 'spec.json').as_uri()), sorted(
            f"{tool['name']}: description differs from the API" for tool in (first, second)))

    def test_live_destructive_drift_fails(self):
        catalog = json.loads((self.root / 'tools.json').read_text())
        cancel = next(t for t in catalog['tools'] if t.get('destructive'))
        other = next(t for t in catalog['tools'] if not t.get('destructive') and not t.get('unavailable'))
        for tool, hint in ((cancel, False), (other, True), (cancel, None), (other, None)):
            with self.subTest(tool=tool['name'], hint=hint):
                spec = live_spec(catalog)
                annotations = spec['paths'][f"/v1/tools/{tool['name']}"]['post']['x-mcp-annotations']
                annotations.pop('destructiveHint')
                if hint is not None:
                    annotations['destructiveHint'] = hint
                (self.root / 'spec.json').write_text(json.dumps(spec))
                errors = check_live(self.root, (self.root / 'spec.json').as_uri())
                self.assertEqual(len(errors), 1)
                self.assertIn(f"{tool['name']}: destructive", errors[0])

    def test_live_count_drift_fails(self):
        catalog = json.loads((self.root / 'tools.json').read_text())
        spec = live_spec(catalog)
        extra = live_operation(catalog['tools'][0])
        spec['paths']['/v1/tools/duplicate'] = {'post': extra}
        (self.root / 'spec.json').write_text(json.dumps(spec))
        self.assertEqual(check_live(self.root, (self.root / 'spec.json').as_uri()),
                         ['count: API lists 39 tools, tools.json lists 38 available'])
        del spec['paths']['/v1/tools/duplicate']
        spec['paths']['/v1/tools/betteroff_new_tool'] = {'post': {'operationId': 'betteroff_new_tool'}}
        (self.root / 'spec.json').write_text(json.dumps(spec))
        errors = check_live(self.root, (self.root / 'spec.json').as_uri())
        self.assertEqual(errors, ['count: API lists 39 tools, tools.json lists 38 available',
                                  'betteroff_new_tool: missing from tools.json'])

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
        self.assertIn('39 tools: 28 read tools and 11 write tools', render(json.loads((ROOT / 'tools.json').read_text())))


    def test_live_skill_input_drift_fails(self):
        catalog = json.loads((self.root / 'tools.json').read_text())
        tools = {t['name']: t for t in catalog['tools']}
        schema = {'properties': {'groupBy': {'type': 'string', 'enum': ['category']}}}
        paths = {f'/v1/tools/{name}': {'post': {
            **live_operation(t),
            'requestBody': {'content': {'application/json': {'schema': schema}}}}} for name, t in tools.items()}
        spec = {'info': {'version': catalog['serverVersion']}, 'paths': paths}
        (self.root / 'spec.json').write_text(json.dumps(spec))
        errors = '\n'.join(check_live(self.root, (self.root / 'spec.json').as_uri()))
        self.assertIn('betteroff_analyze_spending input groupBy does not accept "merchant"', errors)
        self.assertIn('betteroff_get_portfolio has no input includePositions', errors)

if __name__ == '__main__':
    unittest.main()
