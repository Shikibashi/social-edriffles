import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLIENT = ROOT / "upstream" / "social-app"
PDS = ROOT / "upstream" / "atproto-pds" / "packages" / "pds"


class ModerationListPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (PDS / "src/repo/moderation-policy.ts").is_file():
            raise unittest.SkipTest(
                "legacy Radlib moderation policy is outside the pinned Spaces PDS surface"
            )
        cls.fixture = json.loads(
            (ROOT / "tests/fixtures/moderation-list-policy.json").read_text()
        )
        cls.subscribe = (
            CLIENT / "src/screens/ProfileList/components/SubscribeMenu.tsx"
        ).read_text()
        cls.list_queries = (CLIENT / "src/state/queries/list.ts").read_text()
        cls.review = (
            CLIENT / "src/components/dialogs/lists/ReviewListMembersDialog.tsx"
        ).read_text()
        cls.policy = (PDS / "src/repo/moderation-policy.ts").read_text()

    def test_operation_matrix_is_explicit(self):
        by_key = {
            (row["actorPolicy"], row["operation"], row["collection"]): row["expected"]
            for row in self.fixture["operationMatrix"]
        }
        self.assertEqual(
            by_key[("deny-create-update", "create", "app.bsky.graph.listblock")],
            "reject",
        )
        self.assertEqual(
            by_key[("deny-create-update", "update", "app.bsky.graph.listblock")],
            "reject",
        )
        self.assertEqual(
            by_key[("deny-create-update", "delete", "app.bsky.graph.listblock")],
            "allow",
        )
        self.assertEqual(
            by_key[("deny-create-update", "create", "app.bsky.graph.block")],
            "allow",
        )

    def test_client_offers_private_mute_and_explicit_review(self):
        self.assertIn("Mute list", self.subscribe)
        self.assertIn("Review accounts", self.subscribe)
        self.assertNotIn("blockActorList", self.list_queries)
        self.assertNotIn("unblockActorList", self.list_queries)
        self.assertNotIn("useListBlockMutation", self.list_queries)
        self.assertIn("useDirectBlockMutation", self.review)
        self.assertIn("app.bsky.graph.block", self.review)

    def test_standard_lexicon_and_pds_policy_boundary_remain(self):
        self.assertTrue(
            (CLIENT / "src/lexicons/app/bsky/graph/listblock.defs.ts").is_file()
        )
        self.assertIn("LISTBLOCK_COLLECTION", self.policy)
        self.assertIn("deny-create-update", self.policy)
        self.assertIn("Deletes", self.policy)

    def test_attention_and_association_stay_separate_without_a_special_appview(self):
        self.assertIn("useListMuteMutation", self.subscribe)
        self.assertIn("useDirectBlockMutation", self.review)
        self.assertIn("app.bsky.graph.block", self.review)
        self.assertNotIn("blockActorList", self.list_queries)


if __name__ == "__main__":
    unittest.main()
