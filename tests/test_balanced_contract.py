import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BalancedContractTests(unittest.TestCase):
    def test_manifest_fixture_covers_evaluation_regimes(self):
        fixture = json.loads(
            (ROOT / "tests/fixtures/balanced-v1-replay.json").read_text()
        )
        self.assertEqual(fixture["version"], 1)
        self.assertIn("breaking-news", fixture["scenarios"])
        self.assertIn("sybil-flood", fixture["scenarios"])
        self.assertTrue(fixture["expected"]["recordTypeNeutral"])

    def test_balanced_docs_preserve_constitutional_boundaries(self):
        text = (ROOT / "docs/BALANCED_V1.md").read_text()
        self.assertIn("Attention Constitution", text)
        self.assertIn("Portable Personalization", text)
        self.assertIn("chronological", text.lower())
        self.assertIn("harassment amplification", text.lower())
        self.assertIn("Generic ATProto records", text)


if __name__ == "__main__":
    unittest.main()
