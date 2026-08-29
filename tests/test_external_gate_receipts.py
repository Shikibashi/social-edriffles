from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_external_gate_receipts as external  # noqa: E402
import verify_plc_mirror_candidate as plc_candidate  # noqa: E402


class ExternalGateReceiptTests(unittest.TestCase):
    def load(self, name: str) -> dict:
        return external.contract.load_json(ROOT / "tests/fixtures" / name)

    def test_synthetic_private_canary_receipt_passes_contract(self) -> None:
        external.validate_private_canary(
            self.load("external-private-canary-pass.json"), "private-canary"
        )

    def test_synthetic_oauth_expiry_receipt_passes_contract(self) -> None:
        external.validate_oauth_expiry(
            self.load("external-oauth-expiry-pass.json"), "oauth-expiry"
        )

    def test_synthetic_plc_receipt_passes_signature_contract(self) -> None:
        external.validate_plc_independence(
            self.load("external-plc-independence-pass.json"), "plc-independence"
        )

    def test_canary_cannot_claim_private_data_is_absent_when_seen_in_relay(self) -> None:
        receipt = copy.deepcopy(self.load("external-private-canary-pass.json"))
        receipt["checks"]["privateCanaryInRelayStorage"] = True
        with self.assertRaises(AssertionError):
            external.validate_private_canary(receipt, "mutated-canary")

    def test_oauth_cannot_claim_old_refresh_replay_was_rejected_when_accepted(self) -> None:
        receipt = copy.deepcopy(self.load("external-oauth-expiry-pass.json"))
        receipt["checks"]["oldRefreshTokenReplayRejected"] = False
        with self.assertRaises(AssertionError):
            external.validate_oauth_expiry(receipt, "mutated-oauth")

    def test_plc_signature_cannot_be_reused_after_statement_mutation(self) -> None:
        receipt = copy.deepcopy(self.load("external-plc-independence-pass.json"))
        statement = receipt["signedReceipt"]["signedStatement"]
        statement["disagreementWindow"] = "stale"
        receipt["signedReceipt"]["signedPayloadSha256"] = (
            "sha256:" + external.hashlib.sha256(external.canonical_json_bytes(statement)).hexdigest()
        )
        with self.assertRaisesRegex(AssertionError, "signature verification failed"):
            external.validate_plc_independence(receipt, "mutated-plc")

    def test_plc_cannot_claim_independence_for_the_same_operator(self) -> None:
        receipt = copy.deepcopy(self.load("external-plc-independence-pass.json"))
        receipt["operators"]["primary"]["operatorId"] = receipt["operators"]["mirror"][
            "operatorId"
        ]
        with self.assertRaises(AssertionError):
            external.validate_plc_independence(receipt, "same-operator-plc")

    def test_plc_candidate_finds_ed25519_key_after_other_methods(self) -> None:
        key, status = plc_candidate.key_description(
            {
                "verificationMethod": [
                    {"publicKeyMultibase": "zQ3shnon-ed25519-first"},
                    {"publicKeyMultibase": "z6Mkoperator-ed25519"},
                ]
            }
        )
        self.assertEqual(key, "z6Mkoperator-ed25519")
        self.assertEqual(status, "ed25519")

    def test_plc_candidate_reports_missing_operator_key(self) -> None:
        self.assertEqual(
            plc_candidate.key_description({"verificationMethod": []}),
            (None, "operator-key-not-published"),
        )


if __name__ == "__main__":
    unittest.main()
