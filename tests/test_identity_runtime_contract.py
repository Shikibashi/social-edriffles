import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class IdentityRuntimeContractTests(unittest.TestCase):
 def test_matrix_and_docs(self):
  d=json.loads((ROOT/'tests/fixtures/identity-runtime-matrix.json').read_text()); self.assertEqual(len(d['methods']),3); self.assertIn('cache-poisoning',d['security']); self.assertEqual(d['cache']['maxStaleSeconds'],3600)
  t=(ROOT/'docs/IDENTITY_RUNTIME.md').read_text(); self.assertIn('provenance',t); self.assertIn('sensitive writes',t); self.assertIn('simulated',t)
