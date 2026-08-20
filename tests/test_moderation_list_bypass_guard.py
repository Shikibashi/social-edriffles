import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLIENT = ROOT / "upstream" / "social-app"
PDS = ROOT / "upstream" / "atproto-pds" / "packages" / "pds"


class ModerationListBypassGuardTests(unittest.TestCase):
    def test_no_client_bulk_listblock_creation_symbol_remains(self):
        source = "\n".join(
            path.read_text(errors="replace")
            for path in (CLIENT / "src").rglob("*")
            if path.is_file() and path.suffix in {".ts", ".tsx"}
        )
        self.assertNotIn("blockActorList", source)
        self.assertNotIn("unblockActorList", source)
        self.assertNotIn("useListBlockMutation", source)

    def test_list_surfaces_do_not_treat_legacy_listblock_state_as_active(self):
        source = "\n".join(
            (CLIENT / path).read_text(errors="replace")
            for path in (
                "src/screens/List/ListHiddenScreen.tsx",
                "src/screens/ProfileList/components/Header.tsx",
                "src/screens/ProfileList/components/MoreOptionsMenu.tsx",
            )
        )
        self.assertNotIn("list.viewer?.blocked", source)
        self.assertNotIn("Convert list block", source)

    def test_all_mutating_pds_entrypoints_pass_the_policy(self):
        if not (PDS / "src/repo/moderation-policy.ts").is_file():
            raise unittest.SkipTest(
                "legacy Radlib moderation policy is outside the pinned Spaces PDS surface"
            )
        for name in ("createRecord.ts", "putRecord.ts", "applyWrites.ts"):
            source = (PDS / "src/api/com/atproto/repo" / name).read_text()
            self.assertIn("moderationWritePolicy", source, name)
        apply = (PDS / "src/api/com/atproto/repo/applyWrites.ts").read_text()
        delete_branch = apply.split(
            "} else if (com.atproto.repo.applyWrites.delete.$isTypeOf(write))", 1
        )[1]
        self.assertNotIn("moderationWritePolicy", delete_branch.split("} else", 1)[0])

    def test_import_is_not_treated_as_a_normal_write_bypass(self):
        if not (PDS / "src/repo/radlib-migration.ts").is_file():
            raise unittest.SkipTest(
                "legacy Radlib import journal is outside the pinned Spaces PDS surface"
            )
        source = (PDS / "src/api/com/atproto/repo/importRepo.ts").read_text()
        self.assertIn("CAR import does not pass through prepareCreate/prepareUpdate", source)
        self.assertIn("RadlibMigrationJournal", source)
        self.assertIn("markImportFailed", source)


if __name__ == "__main__":
    unittest.main()
