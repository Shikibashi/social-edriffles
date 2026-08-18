import json,subprocess,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class UpstreamHardeningTests(unittest.TestCase):
 def test_baseline_matches_pinned_trees(self):
  p=subprocess.run(['python3','scripts/check_upstream.py','--fast'],cwd=ROOT,text=True,capture_output=True); self.assertEqual(p.returncode,0,p.stdout+p.stderr); d=json.loads(p.stdout); self.assertTrue(d['readOnly']); self.assertTrue(d['ok'])
 def test_delta_and_risk_inventories_are_classified(self):
  delta=json.loads((ROOT/'artifacts/upstream-delta-inventory.json').read_text()); risk=json.loads((ROOT/'artifacts/upstream-rebase-risk.json').read_text()); self.assertTrue(delta['deltas']); self.assertIn('HIGH',{x['risk'] for x in risk['surfaces']}); self.assertEqual(risk['p1'],0)
 def test_untrusted_metadata_is_not_executed(self):
  s=(ROOT/'scripts/check_upstream.py').read_text(); self.assertNotIn('shell=True',s); self.assertNotIn('os.system',s); self.assertIn('networkFetch',subprocess.run(['python3','scripts/check_upstream.py','--fast'],cwd=ROOT,text=True,capture_output=True).stdout)
