import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOCIAL = ROOT / "upstream/social-app/src"
PDS = ROOT / "upstream/atproto-pds/packages/pds/src"


class ProviderBoundaryContractTests(unittest.TestCase):
    def test_appviewlite_is_not_a_tracked_or_configured_dependency(self):
        gitmodules = (ROOT / ".gitmodules").read_text()
        pins = json.loads((ROOT / "upstream-pins.json").read_text())
        tracked = subprocess.run(
            ["git", "ls-files", "upstream/AppViewLite", "upstream/FishyFlip"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertNotIn("AppViewLite", gitmodules)
        self.assertNotIn("FishyFlip", gitmodules)
        self.assertNotIn("appviewlite", pins["repositories"])
        self.assertNotIn("fishyflip", pins["repositories"])
        self.assertEqual(tracked.stdout, "")

        config = subprocess.run(
            [
                "git",
                "config",
                "--get-regexp",
                r"^submodule\.(upstream/AppViewLite|upstream/FishyFlip)\.",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(config.stdout, "")

    def test_client_keeps_appview_as_a_replaceable_generic_provider(self):
        providers = (SOCIAL / "state/session/providers.ts").read_text()
        clients = (SOCIAL / "state/session/clients.ts").read_text()

        self.assertIn("DEFAULT_APPVIEW_PROVIDER", providers)
        self.assertIn("validateAppViewProvider", providers)
        self.assertIn("selectAppViewProvider", providers)
        self.assertIn("probeAppViewProvider", providers)
        self.assertIn("provider.endpoint", clients)
        self.assertNotIn("AppViewLite", providers)
        self.assertNotIn("AppViewLite", clients)

    def test_first_party_pds_owns_repo_and_service_auth_boundaries(self):
        prepare = (PDS / "repo/prepare.ts").read_text()
        create = (PDS / "api/com/atproto/repo/createRecord.ts").read_text()
        put = (PDS / "api/com/atproto/repo/putRecord.ts").read_text()
        apply = (PDS / "api/com/atproto/repo/applyWrites.ts").read_text()
        import_repo = (PDS / "api/com/atproto/repo/importRepo.ts").read_text()
        service_auth = (PDS / "api/com/atproto/server/getServiceAuth.ts").read_text()

        for source in (prepare, create, put, apply, import_repo):
            self.assertIn("repo", source.lower())
        self.assertIn("com.atproto.server.getServiceAuth", service_auth)
        self.assertIn("createServiceJwt", service_auth)

    def test_moderation_list_attention_remains_client_local(self):
        subscribe = (
            SOCIAL / "screens/ProfileList/components/SubscribeMenu.tsx"
        ).read_text()
        list_queries = (SOCIAL / "state/queries/list.ts").read_text()
        review = (
            SOCIAL / "components/dialogs/lists/ReviewListMembersDialog.tsx"
        ).read_text()

        self.assertIn("useListMuteMutation", subscribe)
        self.assertIn("useListMuteMutation", list_queries)
        self.assertIn("useDirectBlockMutation", review)
        self.assertIn("app.bsky.graph.block", review)
        self.assertNotIn("blockActorList", list_queries)
        self.assertNotIn("unblockActorList", list_queries)


if __name__ == "__main__":
    unittest.main()
