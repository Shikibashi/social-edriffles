import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
OBSERVATIONS = ROOT / "artifacts/service-auth-security-observations.json"


class LiveServiceAuthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.observations = json.loads(OBSERVATIONS.read_text())
        cls.results = cls.observations["results"]

    def test_valid_token_is_accepted_once(self):
        self.assertEqual(self.results["valid_first"], 200)

    def test_replay_and_raw_access_token_are_rejected(self):
        self.assertNotEqual(self.results["valid_replay"], 200)
        self.assertNotEqual(self.results["raw_pds_access"], 200)

    def test_signature_and_claim_mismatches_are_rejected(self):
        self.assertNotEqual(self.results["bad_signature"], 200)
        self.assertNotEqual(self.results["wrong_audience"], 200)
        self.assertNotEqual(self.results["wrong_lxm"], 200)
        self.assertIn("expired_issuance_error", self.results)


if __name__ == "__main__":
    unittest.main()
