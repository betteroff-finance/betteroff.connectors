"""Render docs/tools.md from tools.json and check the catalog against the skills, docs, and live API.

Usage: python3 scripts/tools_catalog.py [--check] [--live]
  (no flag)  rewrite docs/tools.md
  --check    fail if docs/tools.md is stale or any skill or document disagrees with tools.json
  --live     fail if the public OpenAPI tool operations disagree with tools.json, or a skill passes
             an input name or enum value a tool does not accept (needs network)
"""
import argparse
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = re.compile(r'betteroff_[a-z][a-z_]*')
# A skill step such as: Call `betteroff_analyze_spending` with `groupBy: "merchant"`.
CALL = re.compile(r'`(betteroff_[a-z_]+)`[^`]*((?:`[^`]+`[^`]*)+)')
INPUT = re.compile(r'`([A-Za-z]+): ("[^"]*"|true|false|\d+)`')


def load(root):
    return json.loads((root / 'tools.json').read_text())


def render(catalog):
    tools = catalog['tools']
    writes = sum(not t['readOnly'] for t in tools)
    rows = '\n'.join(
        f"| `{t['name']}` | {'Read' if t['readOnly'] else 'Write'} "
        f"| {', '.join(f'`{s}`' for s in t['scopes'])} | {t['summary']} |"
        for t in tools)
    return f"""<!-- Generated from tools.json by scripts/tools_catalog.py. Edit tools.json, then run the script. -->
<picture><source media="(prefers-color-scheme: dark)" srcset="../assets/betteroff-mark-white.svg"><img src="../assets/betteroff-mark-graphite.svg" alt="" width="40" height="40"></picture>

# BetterOff tools

[All clients](../README.md#install-the-connector) · [Connector reference](connector.md)

Connector package {catalog['version']} describes hosted server {catalog['serverVersion']} at `{catalog['server']}` and defines {len(tools)} tools: {len(tools) - writes} read tools and {writes} write tools. A client sees only the tools its granted scopes allow.

- **Read** tools return data and change nothing.
- **Write** tools save a pending correction or transfer request, cancel a pending request, or send feedback. None can apply a correction, approve a transfer, or sign a transaction. You do those in BetterOff. Cancellation and feedback take effect when called.
- Every tool requires BetterOff Core, over MCP or REST. The Free plan and trials do not include tool access.

The same catalog is available as [tools.json](../tools.json). With an API token, call any tool at `POST https://api.betteroff.finance/v1/tools/{{name}}`; see the [developer documentation](https://betteroff.finance/developers) and the [tool OpenAPI document]({catalog['openapi']}).

| Tool | Access | Scopes | Description |
| --- | --- | --- | --- |
{rows}
"""


def table_tools(skill):
    return set(re.findall(r'^\|[^|]*\| `(betteroff_[a-z_]+)` \|$', skill.read_text(), re.M))


def check(root):
    catalog = load(root)
    names = [t['name'] for t in catalog['tools']]
    errors = []
    if len(set(names)) != len(names):
        errors.append('tools.json: duplicate tool names')
    if (root / 'docs/tools.md').read_text() != render(catalog):
        errors.append('docs/tools.md is stale; run python3 scripts/tools_catalog.py')
    for skill in ('plugins/betteroff/skills/household-review/SKILL.md', 'skills/household-review/SKILL.md'):
        listed = table_tools(root / skill)
        if listed != set(names):
            errors.append(f'{skill}: tool table differs from tools.json: '
                          f'missing {sorted(set(names) - listed)}, extra {sorted(listed - set(names))}')
    sources = [root / 'README.md', root / 'AGENTS.md', root / 'plugins/betteroff/plugin.json',
               *root.glob('docs/**/*.md'), *root.glob('plugins/betteroff/skills/**/*'), *root.glob('integrations/**/*')]
    for path in sources:
        if path.is_file() and path.suffix in ('.md', '.json', '.yaml', '.cjs'):
            for name in sorted(set(TOOL.findall(path.read_text())) - set(names)):
                errors.append(f'{path.relative_to(root)}: unknown tool {name}')
    if not re.search(rf'(?<!\d){len(names)} tools\b', (root / 'README.md').read_text()):
        errors.append(f'README.md must state "{len(names)} tools"')
    return errors


def check_live(root, url=None):
    catalog = load(root)
    with urllib.request.urlopen(url or catalog['openapi'], timeout=30) as response:
        spec = json.load(response)
    live = {}
    for path, item in spec['paths'].items():
        operation = item.get('post', {})
        if path.startswith('/v1/tools/') and not operation.get('deprecated'):
            live[operation['operationId']] = operation
    errors = []
    if not spec['info']['version'].split('+')[0] == catalog['serverVersion']:
        errors.append(f"version: API {spec['info']['version']} != tools.json serverVersion {catalog['serverVersion']}")
    expected = {t['name']: t for t in catalog['tools']}
    for name in sorted(set(live) ^ set(expected)):
        errors.append(f"{name}: {'missing from tools.json' if name in live else 'missing from the API'}")
    for name in sorted(set(live) & set(expected)):
        tool, operation = expected[name], live[name]
        if operation.get('summary') != tool['title']:
            errors.append(f"{name}: title {tool['title']!r} != API {operation.get('summary')!r}")
        read_only = operation.get('x-mcp-annotations', {}).get('readOnlyHint')
        if read_only is not tool['readOnly']:
            errors.append(f"{name}: readOnly {tool['readOnly']!r} != API readOnlyHint {read_only!r}")
        scopes = {s for requirement in operation.get('security', []) for s in requirement.get('agentOAuth', [])}
        if scopes != set(tool['scopes']):
            errors.append(f"{name}: scopes {sorted(tool['scopes'])} != API {sorted(scopes)}")
    errors += check_skill_inputs(root, live)
    return errors


def check_skill_inputs(root, live):
    """Inputs a skill writes next to a tool name must exist on that tool, and match its enum."""
    errors = []
    for path in sorted({*root.glob('skills/**/SKILL.md'), *root.glob('plugins/betteroff/skills/**/SKILL.md')}):
        for line in path.read_text().splitlines():
            for name, rest in CALL.findall(line):
                properties = (live.get(name, {}).get('requestBody', {}).get('content', {})
                              .get('application/json', {}).get('schema', {}).get('properties'))
                if properties is None:
                    continue
                for key, value in INPUT.findall(rest):
                    where = f'{path.relative_to(root)}: {name}'
                    if key not in properties:
                        errors.append(f'{where} has no input {key}')
                    elif value.startswith('"') and 'enum' in properties[key] \
                            and value.strip('"') not in properties[key]['enum']:
                        errors.append(f'{where} input {key} does not accept {value}')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    if not (args.check or args.live):
        (ROOT / 'docs/tools.md').write_text(render(load(ROOT)))
        parser.exit(0, 'Updated docs/tools.md\n')
    problems = (check(ROOT) if args.check else []) + (check_live(ROOT) if args.live else [])
    parser.exit(1 if problems else 0, '\n'.join(problems or ['Tool catalog passed']) + '\n')
