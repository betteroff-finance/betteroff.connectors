import json
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile
from package_chatgpt import build, SOURCE

class ChatgptPackageTest(unittest.TestCase):
    def test_package_preserves_shared_source(self):
        before = (SOURCE / 'plugin.json').read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            with ZipFile(build(Path(directory) / 'chatgpt.zip')) as archive:
                mcp = json.loads(archive.read('mcp.json'))
                self.assertEqual(mcp['mcpServers']['betteroff']['url'], 'https://api.betteroff.finance/mcp')
                manifest = json.loads(archive.read('plugin.json'))
                self.assertEqual(manifest, json.loads(before))
                listing = manifest['extensions']['com.openai']
                self.assertEqual(len(listing['review']['test_cases']['positive']), 5)
                self.assertEqual(len(listing['review']['test_cases']['negative']), 3)
                skills = sorted(p.relative_to(SOURCE).as_posix() for p in (SOURCE / 'skills').rglob('*') if p.is_file())
                self.assertEqual(sorted(e for e in archive.namelist() if e.startswith('skills/')), skills)
                for entry in skills:
                    self.assertEqual(archive.read(entry), (SOURCE / entry).read_bytes())
                skill = archive.read('skills/household-review/SKILL.md').decode()
                self.assertIn('individualized investment, tax, or legal advice', skill)
                self.assertIn('DeFi, and prepares corrections for review in BetterOff. Use for general '
                              'financial questions', skill)
        self.assertEqual(before, (SOURCE / 'plugin.json').read_bytes())

if __name__ == '__main__':
    unittest.main()
