import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class IdentityConstitutionTests(unittest.TestCase):
 def test_contract_boundaries_and_adversarial_cases(self):
  c=json.loads((ROOT/'tests/fixtures/identity-contract.json').read_text()); a=json.loads((ROOT/'tests/fixtures/identity-adversarial.json').read_text())
  self.assertEqual(c['version'],1); self.assertIn('did',c['authorities']['identity']); self.assertGreaterEqual(len(a['cases']),18)
 def test_exit_harness(self):
  import sys; sys.path.insert(0,str(ROOT/'tests/exit')); from identity_exit_harness import run
  r=run(); self.assertTrue(r['didContinuous']); self.assertTrue(r['preferencesRestored']); self.assertFalse(r['credentialsExported'])
 def test_documents_define_boundaries(self):
  t=(ROOT/'docs/IDENTITY_CONSTITUTION.md').read_text(); self.assertIn('DID',t); self.assertIn('Recovery',t); self.assertIn('Identity != handle',t)
