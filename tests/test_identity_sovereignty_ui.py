import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class IdentitySovereigntyUiTests(unittest.TestCase):
    def test_fixture_covers_required_surfaces(self):
        d = json.loads(
            (ROOT / "tests/fixtures/identity-sovereignty-ui.json").read_text()
        )
        self.assertGreaterEqual(len(d["screens"]), 10)
        self.assertTrue(d["privacy"]["secretsRedacted"])

    def test_docs_preserve_simulation_and_domains(self):
        t = (ROOT / "docs/IDENTITY_SOVEREIGNTY_UI.md").read_text()
        self.assertIn("Simulated", t)
        self.assertIn("portable personalization", t)
