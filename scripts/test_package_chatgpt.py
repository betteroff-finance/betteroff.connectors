import json
import shutil
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile
import package_chatgpt
from package_chatgpt import build, SOURCE, TRANSFER_TOOLS

class ChatgptPackageTest(unittest.TestCase):
    def test_restricted_package_preserves_shared_source(self):
        before = (SOURCE / 'plugin.json').read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            with ZipFile(build(Path(directory) / 'chatgpt.zip')) as archive:
                mcp = json.loads(archive.read('mcp.json'))
                self.assertEqual(mcp['mcpServers']['betteroff']['url'], 'https://api.betteroff.finance/mcp')
                for entry in archive.namelist():
                    if entry.startswith('skills/'):
                        self.assertNotIn('<!-- transfers', archive.read(entry).decode())
                        self.assertNotIn('prepare bank transfers', archive.read(entry).decode())
                        for name in TRANSFER_TOOLS:
                            self.assertNotIn(name, archive.read(entry).decode())
                        self.assertNotIn('transfers:bank', archive.read(entry).decode())
                manifest = json.loads(archive.read('plugin.json'))
                listing = manifest['extensions']['com.openai']
                self.assertEqual(len(listing['review']['test_cases']['positive']), 5)
                self.assertEqual(len(listing['review']['test_cases']['negative']), 3)
                self.assertNotIn('With separate transfer permission', listing['interface']['longDescription'])
                skill = archive.read('skills/household-review/SKILL.md').decode()
                self.assertIn('individualized investment, tax, or legal advice', skill)
                self.assertIn('DeFi, and prepares corrections for review in BetterOff. Use for general '
                              'financial questions', skill)
                for name in TRANSFER_TOOLS:
                    self.assertNotIn(name, skill)
                self.assertNotIn('transfers:bank', skill)
        self.assertEqual(before, (SOURCE / 'plugin.json').read_bytes())

    def build_with(self, directory, name, text):
        copy = Path(directory) / 'betteroff'
        shutil.copytree(SOURCE, copy)
        target = copy / 'skills/monthly-review' / name
        target.write_text((target.read_text() if target.exists() else '') + text)
        self.addCleanup(setattr, package_chatgpt, 'SOURCE', SOURCE)
        package_chatgpt.SOURCE = copy
        return build(Path(directory) / 'chatgpt.zip')

    def test_nested_transfer_block_fails(self):
        nested = ('<!-- transfers -->\na\n<!-- transfers -->\nb\n<!-- /transfers -->\n'
                  'Wallet transfer text\n<!-- /transfers -->\n')
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, 'Transfer tool remains'):
                self.build_with(directory, 'SKILL.md', nested)

    def test_transfer_tool_in_unfiltered_file_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, 'unfiltered file'):
                self.build_with(directory, 'reference.txt', 'Call betteroff_request_bank_transfer.\n')

if __name__ == '__main__':
    unittest.main()
