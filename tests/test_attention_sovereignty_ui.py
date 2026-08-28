import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AttentionSovereigntyUiTests(unittest.TestCase):
    def test_fixture_covers_user_surfaces(self):
        data = json.loads(
            (ROOT / "tests/fixtures/attention-sovereignty-ui.json").read_text()
        )
        self.assertIn("feed-provenance", data["screens"])
        self.assertIn("why-this-post", data["screens"])
        self.assertFalse(data["privacy"]["confidentialIntegrityVisible"])

    def test_docs_preserve_boundaries(self):
        text = (ROOT / "docs/ATTENTION_SOVEREIGNTY_UI_V1.md").read_text()
        self.assertIn("account-scoped", text)
        self.assertIn("confidential integrity", text)
        self.assertIn("accessible", text)


if __name__ == "__main__":
    unittest.main()
