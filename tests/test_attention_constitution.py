import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AttentionConstitutionTests(unittest.TestCase):
    def test_machine_contract_classifies_all_surfaces(self):
        contract = json.loads(
            (ROOT / "tests/fixtures/attention-contract.json").read_text()
        )
        self.assertEqual(contract["version"], 1)
        self.assertEqual(len(contract["surfaces"]), 10)
        self.assertIn("confidential-anti-abuse", contract["explanationScopes"])
        self.assertIn("durable-account-mutation", contract["authorityClasses"])
        self.assertIn(
            "dogpile-amplification-control", contract["concentrationControls"]
        )

    def test_constitution_preserves_frozen_boundaries(self):
        text = (ROOT / "docs/ATTENTION_CONSTITUTION.md").read_text()
        self.assertIn("Portable Personalization v1", text)
        self.assertIn("Service Constitution", text)
        self.assertIn("Association Constitution", text)
        self.assertIn("Chronological access", text)
        self.assertIn("Public scope", text)
        self.assertIn("Audit scope", text)
        self.assertIn("Confidential scope", text)
        self.assertIn("Emergency authority", text)
        self.assertIn("author caps", text.lower())

    def test_personalization_and_service_sources_preserve_boundaries(self):
        personalization = (
            ROOT / "upstream/social-app/src/lib/personalization.ts"
        ).read_text()
        providers = (
            ROOT / "upstream/social-app/src/state/session/providers.ts"
        ).read_text()
        self.assertIn("PERSONALIZATION_FORMAT", personalization)
        self.assertIn("encryptPersonalization", personalization)
        self.assertIn("importPersonalization", personalization)
        self.assertIn("rejectCredentialValue", personalization)
        self.assertIn("validateAppViewProvider", providers)
        self.assertIn("selectAppViewProvider", providers)


if __name__ == "__main__":
    unittest.main()
