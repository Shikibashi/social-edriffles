import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPVIEW = ROOT / "upstream" / "AppViewLite"

class AppViewLiteCharacterizationTests(unittest.TestCase):
    """Static characterization for the pinned source baseline.

    Live endpoint evidence is recorded separately in artifacts/live-ab-c-characterization.json.
    """

    @classmethod
    def setUpClass(cls):
        cls.matrix = json.loads((ROOT / "tests/fixtures/blocking-matrix.json").read_text())
        cls.source_files = [p for p in APPVIEW.rglob("*") if p.is_file() and p.suffix in {".cs", ".razor", ".js"}]
        cls.source = "\n".join(f"{p}\n{p.read_text(errors='replace')}" for p in cls.source_files)

    def test_pinned_source_exists(self):
        self.assertTrue(APPVIEW.is_dir())
        self.assertIn(self.matrix["baseline"].split("@")[1], "75f78e8e098c05f52821e836832205050c0f539e")

    def test_fixture_surfaces_have_source_evidence(self):
        evidence = {
            "posts": "PostRow",
            "threads": "ProfilePage",
            "profiles": "ProfilePage",
            "follows": "FollowButton",
            "replies": "CanReply",
            "mentions": "Mention",
            "notifications": "Notification",
            "quotes": "Quote",
            "feeds": "Feed",
            "block-list": "ProfileBlocking",
            "blocked-by": "ProfileBlockedBy",
        }
        for surface in self.matrix["surfaces"]:
            needle = evidence[surface]
            self.assertIn(needle.lower(), self.source.lower(), f"no pinned-source evidence for {surface}")

    def test_three_account_contract_is_complete(self):
        self.assertEqual({row["viewer"] for row in self.matrix["rows"]}, {"A", "B", "C"})
        for surface in self.matrix["surfaces"]:
            self.assertTrue(any(row["surface"] == surface for row in self.matrix["rows"]))
    def test_block_relationship_is_pairwise_and_symmetric(self):
        relationships = (APPVIEW / "src/AppViewLite/BlueskyRelationships.cs").read_text()
        self.assertIn("UsersHavePairwiseBlockRelationshipCore", relationships)
        self.assertIn("UserBlocksUser(a, b, ctx)", relationships)
        self.assertIn("UserBlocksUser(b, a, ctx)", relationships)
        self.assertIn("if (a == b) return default;", relationships)

    def test_get_blocks_endpoint_is_implemented(self):
        controller = (APPVIEW / "src/AppViewLite.Web/ApiCompat/AppBskyGraph.cs").read_text()
        self.assertIn("GetBlockingAsync", controller)
        self.assertIn("Blocks = blocks.Select", controller)
        body = controller.split("GetBlocksAsync", 1)[1].split("GetFollowersAsync", 1)[0]
        self.assertNotIn("throw new NotImplementedException()", body)
if __name__ == "__main__":
    unittest.main()
