import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ExperimentalAttentionTests(unittest.TestCase):
 def test_five_opt_in_modules_and_baselines(self):
  d=json.loads((ROOT/'tests/fixtures/experimental-attention-v1.json').read_text()); self.assertEqual(len(d['modules']),5); self.assertTrue(d['optIn']); self.assertEqual(set(d['baselines']),{'chronological','engagement','balanced'})
 def test_docs_state_experimental_limitations(self):
  t=(ROOT/'docs/EXPERIMENTAL_ATTENTION_MODULES_V1.md').read_text(); self.assertIn('experimental',t); self.assertIn('chronological',t); self.assertIn('limitations',t)
