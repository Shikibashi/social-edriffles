import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class RadlibAcceptanceTests(unittest.TestCase):
 def test_traceability_covers_all_24_and_partial_is_explicit(self):
  d=json.loads((ROOT/'artifacts/radlib-principle-traceability.json').read_text()); self.assertEqual(len(d['principles']),24); self.assertTrue(any(x['status']=='PARTIAL' for x in d['principles'])); self.assertEqual(d['acceptanceState'],'AUTOMATED_ACCEPTANCE_PASSED')
 def test_owner_acceptance_pending(self):
  d=json.loads((ROOT/'tests/fixtures/radlib-owner-intent.json').read_text()); self.assertEqual(d['acceptanceState'],'OWNER_ACCEPTANCE_PENDING'); t=(ROOT/'docs/OWNER_ACCEPTANCE_CHECKLIST.md').read_text(); self.assertGreaterEqual(len(re.findall(r'^\|\s*\d+\s*\|',t,re.M)),30)
 def test_neutrality_and_credentials(self):
  files=list((ROOT/'artifacts').glob('radlib*.json'))+[ROOT/'tests/fixtures/radlib-owner-intent.json']; text='\n'.join(p.read_text() for p in files); self.assertNotRegex(text,r'left.?right\s*quota|demographic\s*quota'); self.assertNotIn('refreshJwt',text); self.assertNotIn('privateKey',text)
