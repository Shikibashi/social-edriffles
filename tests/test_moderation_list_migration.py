import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLIENT = ROOT / "upstream" / "social-app"
PDS = ROOT / "upstream" / "atproto-pds" / "packages" / "pds"


class ModerationListMigrationTests(unittest.TestCase):
    def test_required_order_and_failure_invariants_are_fixture_backed(self):
        fixture = json.loads(
            (ROOT / "tests/fixtures/moderation-list-migration.json").read_text()
        )
        self.assertEqual(
            fixture["ordering"][:4],
            [
                "create-private-list-mute",
                "verify-private-list-mute",
                "delete-public-listblock-with-cas",
                "verify-public-listblock-deletion",
            ],
        )
        self.assertEqual(fixture["failureInvariants"]["muteFailure"], "source-listblock-remains")
        self.assertEqual(fixture["failureInvariants"]["directBlocksWithoutReview"], "unchanged")

    def test_client_migration_has_safe_order_and_cas_delete(self):
        source = (CLIENT / "src/state/queries/list.ts").read_text()
        mute = source.index("muteActorList")
        verify_mute = source.index("verifyPrivateListMute", mute)
        delete = source.index("deleteRecord", verify_mute)
        verify_delete = source.index("isRecordNotFoundError", delete)
        self.assertLess(mute, verify_mute)
        self.assertLess(verify_mute, delete)
        self.assertLess(delete, verify_delete)
        self.assertIn("swapRecord: record.cid", source)
        self.assertIn("directBlocksBefore", source)
        self.assertIn(
            "directBlockDelta",
            (CLIENT / "src/lib/moderation/listblock-migration.ts").read_text(),
        )

    def test_pds_journal_is_receipt_only_and_retryable(self):
        journal = (PDS / "src/repo/radlib-migration.ts").read_text()
        self.assertIn("radlib-listblock-migration/1", journal)
        self.assertIn("sourceUriHash", journal)
        self.assertIn("subjectListUriHash", journal)
        self.assertIn("markImportFailed", journal)
        self.assertIn("reconcile", journal)
        self.assertIn("mode: 0o600", journal)
        self.assertNotIn("password", journal.lower())
        self.assertNotIn("accessToken", journal)


if __name__ == "__main__":
    unittest.main()
