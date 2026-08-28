import json
import unittest
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]


class ConstitutionalStackIntegrationTests(unittest.TestCase):
    def load(self, n: str) -> dict[str, Any]:
        return cast(
            dict[str, Any],
            json.loads((ROOT / "tests/fixtures" / n).read_text()),
        )

    def test_authority_invariants(self):
        d = self.load("constitutional-stack-authority.json")
        self.assertIn("feed-advice-does-not-create-association", d["invariants"])
        self.assertEqual(
            d["actors"]["feed-provider"]["Association"], ["MAY_NOT_EXERCISE"]
        )

    def test_data_flow_forbids_credentials(self):
        d = self.load("constitutional-stack-data-flow.json")
        self.assertGreaterEqual(len(d["forbidden"]), 4)
        self.assertNotIn("refresh_token", json.dumps(d))

    def test_capability_matrix_is_explicit(self):
        d = self.load("constitutional-stack-capabilities.json")
        self.assertEqual(len(d["transitions"]), 5)
        self.assertIn("SIMULATED", [x["class"] for x in d["transitions"]])
