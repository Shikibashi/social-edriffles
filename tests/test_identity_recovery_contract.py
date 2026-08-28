import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class IdentityRecoveryContractTests(unittest.TestCase):
    def test_fixture_and_docs(self):
        d = json.loads((ROOT / "tests/fixtures/identity-recovery.json").read_text())
        self.assertEqual(d["version"], 1)
        self.assertFalse(d["secretsInReceipts"])
        self.assertGreaterEqual(len(d["adversarialCases"]), 13)
        t = (ROOT / "docs/IDENTITY_RECOVERY.md").read_text()
        self.assertIn("not a new universal identity authority", t)
        self.assertIn("lockdown", t)
