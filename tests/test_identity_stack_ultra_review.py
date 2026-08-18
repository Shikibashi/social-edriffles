import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class IdentityStackUltraReviewTests(unittest.TestCase):
 def test_blocking_findings_are_explicit(self):
  d=json.loads((ROOT/'artifacts/identity-stack-v1-ultra-review.json').read_text()); self.assertEqual(d['verdict'],'IDENTITY_STACK_V1_REVIEW_BLOCKED'); self.assertEqual(d['severity']['P1'],3); self.assertIn('unhardened resolver endpoints',d['findings'])
 def test_report_classifies_simulated_work(self):
  t=(ROOT/'docs/IDENTITY_STACK_V1_RELEASE_REVIEW.md').read_text(); self.assertIn('SIMULATED',t); self.assertIn('SKIPPED_ENVIRONMENT',t); self.assertIn('Required remediation',t)
