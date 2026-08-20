import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDS = ROOT / "upstream" / "atproto-pds" / "packages" / "pds"
ACCOUNT_MANAGER = PDS / "src/account-manager/account-manager.ts"


class ModerationListImportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (PDS / "src/repo/moderation-policy.ts").is_file():
            raise unittest.SkipTest(
                "legacy Radlib moderation policy is outside the pinned Spaces PDS surface"
            )
        cls.fixture = json.loads(
            (ROOT / "tests/fixtures/moderation-list-import.json").read_text()
        )
        cls.import_path = (
            PDS / "src/api/com/atproto/repo/importRepo.ts"
        ).read_text()
        cls.status_path = (
            PDS / "src/api/com/atproto/sync/getRepoStatus.ts"
        ).read_text()
        cls.account_manager_path = ACCOUNT_MANAGER.read_text()

    def test_import_fixture_is_truthful_about_the_boundary(self):
        self.assertIn("inventory listblocks before commit", self.fixture["pdsBehavior"])
        self.assertIn("client creates/verifies private mute", self.fixture["postImportMigration"])
        self.assertIn("automatic provider-side mute conversion", self.fixture["activationTruth"])

    def test_car_import_has_a_distinct_inventory_path(self):
        self.assertIn("verifyDiff", self.import_path)
        self.assertIn("inventoryListblocks", self.import_path)
        self.assertIn("beginImport", self.import_path)
        self.assertIn("markImportComplete", self.import_path)
        self.assertIn("markImportFailed", self.import_path)
        self.assertIn("LISTBLOCK_COLLECTION", self.import_path)

    def test_repository_status_reconciles_only_after_records_are_gone(self):
        self.assertIn("countRecordsForCollection", self.status_path)
        self.assertIn("journal.reconcile", self.status_path)
        self.assertIn("cannot fabricate provider-side mute state", self.status_path)

    def test_account_activation_is_gated_on_repository_cleanup(self):
        self.assertIn("assertRadlibMigrationReady", self.account_manager_path)
        self.assertIn("RadlibMigrationPending", self.account_manager_path)
        self.assertIn(
            "Account activation is blocked until legacy listblocks are migrated",
            self.account_manager_path,
        )
        self.assertIn("countRecordsForCollection", self.account_manager_path)


if __name__ == "__main__":
    unittest.main()
