"""Generate the ChatGPT submission ZIP from the shared plugin."""
import json
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / 'plugins/betteroff/plugin.json').exists())
SOURCE = ROOT / 'plugins/betteroff'


def build(output):
    manifest = json.loads((SOURCE / 'plugin.json').read_text())
    mcp = json.loads((SOURCE / 'mcp.json').read_text())
    # OpenAI fixes this URL at registration. The API restricts the verified ChatGPT client.
    mcp['mcpServers']['betteroff']['url'] = 'https://api.betteroff.finance/mcp'
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
        archive.writestr('plugin.json', json.dumps(manifest, indent=2) + '\n')
        archive.writestr('mcp.json', json.dumps(mcp, indent=2) + '\n')
        archive.writestr('README.md', '# Better Off for ChatGPT\n\nRead household finances and prepare corrections for approval in Better Off.\n')
        for path in sorted(SOURCE.rglob('*')):
            relative = path.relative_to(SOURCE)
            if path.is_file() and relative.parts[0] in ('skills', 'assets'):
                archive.write(path, relative)
    return output


if __name__ == '__main__':
    print(build(sys.argv[1]))
