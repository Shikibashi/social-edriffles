import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class AttentionStackReleaseAuditTests(unittest.TestCase):
 def test_audit_is_blocked_by_explicit_p1_findings(self):
  d=json.loads((ROOT/'artifacts/attention-stack-v1-release-audit.json').read_text())
  self.assertEqual(d['decision'],'ATTENTION_STACK_V1_REVIEW_BLOCKED'); self.assertGreaterEqual(len(d['p1']),1)
  t=(ROOT/'docs/ATTENTION_STACK_V1_RELEASE_AUDIT.md').read_text(); self.assertIn('P1',t); self.assertIn('ATTENTION_STACK_V1_REVIEW_BLOCKED',t)
