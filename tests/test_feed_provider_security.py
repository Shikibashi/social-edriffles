import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FeedProviderSecurityContractTests(unittest.TestCase):
    def test_adversarial_matrix_is_complete_and_data_only(self):
        fixture = json.loads(
            (ROOT / "tests/fixtures/feed-provider-security.json").read_text()
        )
        expected = {
            "huge-response",
            "huge-compressed-response",
            "excessive-candidates",
            "malicious-cursor",
            "invalid-uri",
            "invalid-cid",
            "duplicate-candidate",
            "stale-batch",
            "redirect-abuse",
            "slow-provider",
            "unavailable-provider",
            "forged-provider-identity",
            "invalid-manifest-signature",
            "revoked-key",
            "malformed-reason",
            "hydration-mismatch",
            "executable-payload",
            "relationship-immutability",
        }
        self.assertTrue(expected <= set(fixture["cases"]))
        self.assertTrue(fixture["dataOnly"])

    def test_security_docs_preserve_frozen_constitutions(self):
        threat = (ROOT / "docs/FEED_PROVIDER_THREAT_MODEL.md").read_text()
        security = (ROOT / "docs/FEED_PROVIDER_SECURITY.md").read_text()
        for text in (threat, security):
            self.assertIn("Attention Constitution", text)
            self.assertIn("Portable Personalization", text)
            self.assertIn("Candidate Protocol v1", text)
            self.assertIn("executable", text.lower())


if __name__ == "__main__":
    unittest.main()
