import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class IdentityStackUltraReviewTests(unittest.TestCase):
    def test_remediation_clears_release_blockers(self):
        d = json.loads(
            (ROOT / "artifacts/identity-stack-v1-ultra-review.json").read_text()
        )
        self.assertEqual(d["verdict"], "IDENTITY_STACK_V1_RELEASE_READY")
        self.assertEqual(d["severity"]["P1"], 0)
        self.assertTrue(d["remediation"]["endpointValidation"])
        self.assertTrue(d["remediation"]["freshAuthorizationCache"])

    def test_report_classifies_limitations(self):
        t = (ROOT / "docs/IDENTITY_STACK_V1_RELEASE_REVIEW.md").read_text()
        self.assertIn("SIMULATED", t)
        self.assertIn("SKIPPED_ENVIRONMENT", t)
        self.assertIn("P2/P3 findings", t)
