"""Generate the restricted ChatGPT submission ZIP from the shared plugin."""
import json
import re
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / 'plugins/betteroff/plugin.json').exists())
SOURCE = ROOT / 'plugins/betteroff'
TRANSFER_TOOLS = ('betteroff_request_bank_transfer', 'betteroff_get_action_request',
                  'betteroff_cancel_action_request')
# Skills mark transfer-only text with these lines; the package drops the marked blocks.
TRANSFER_BLOCK = re.compile(r'^<!-- transfers -->\n.*?^<!-- /transfers -->\n', re.M | re.S)


def replace_once(text, old, new):
    # Fail loudly when the source wording changes instead of silently shipping transfer text.
    if text.count(old) != 1:
        raise ValueError(f'Expected one occurrence of {old!r}')
    return text.replace(old, new)


def build(output):
    manifest = json.loads((SOURCE / 'plugin.json').read_text())
    manifest['description'] = 'See household finances and prepare corrections for approval in BetterOff.'
    listing = manifest['extensions']['com.openai']
    interface = listing['interface']
    interface['capabilities'] = [item for item in interface['capabilities'] if 'transfer' not in item.lower()]
    description = interface['longDescription']
    start = description.index('With separate transfer permission,')
    end = description.index('The plugin cannot', start)
    interface['longDescription'] = description[:start] + description[end:]
    listing['publication']['release_notes'] = 'ChatGPT cannot access transfer tools. Read household finances and prepare corrections for approval in BetterOff.'
    listing['review']['test_cases']['negative'][0] = {
        'prompt': 'Send 10 USDC to my other wallet.',
        'description': 'This ChatGPT plugin cannot request or execute bank or crypto transfers. Explain that limitation, call no transfer tool, and claim no transfer.'
    }
    mcp = json.loads((SOURCE / 'mcp.json').read_text())
    # OpenAI fixes this URL at registration. The API restricts the verified ChatGPT client.
    mcp['mcpServers']['betteroff']['url'] = 'https://api.betteroff.finance/mcp'
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
        archive.writestr('plugin.json', json.dumps(manifest, indent=2) + '\n')
        archive.writestr('mcp.json', json.dumps(mcp, indent=2) + '\n')
        archive.writestr('README.md', '# BetterOff for ChatGPT\n\nRead household finances and prepare corrections for approval in BetterOff. Transfers are unavailable.\n')
        for path in sorted(SOURCE.rglob('*')):
            relative = path.relative_to(SOURCE)
            if not path.is_file() or relative.parts[0] not in ('skills', 'assets'):
                continue
            if path.suffix in ('.md', '.yaml'):
                text = re.sub(r'\n{3,}', '\n\n', TRANSFER_BLOCK.sub('', path.read_text()))
                if relative == Path('skills/household-review/SKILL.md'):
                    text = replace_once(text, 'prepares corrections and transfer requests for', 'prepares corrections for')
                    text += '\nThis ChatGPT plugin cannot request, approve, sign, or execute transfers.\n'
                if 'transfers -->' in text or 'transfers:' in text or any(tool in text for tool in TRANSFER_TOOLS):
                    raise ValueError(f'Transfer tool remains in {relative}')
                archive.writestr(str(relative), text)
            else:
                # Only .md and .yaml files are filtered, so reject transfer text in any other file.
                data = path.read_bytes()
                if b'transfers' in data or any(tool.encode() in data for tool in TRANSFER_TOOLS):
                    raise ValueError(f'Transfer text in unfiltered file {relative}')
                archive.write(path, relative)
    return output


if __name__ == '__main__':
    print(build(sys.argv[1]))
