import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
OBSERVATIONS = ROOT / "artifacts/live-block-presentation-observations.json"
SURFACES = ROOT / "artifacts/live-block-presentation-surface-summary.json"
MATRIX = ROOT / "docs/LIVE_BLOCK_PRESENTATION_MATRIX.md"


class LiveBlockPresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.observations = json.loads(OBSERVATIONS.read_text())
        cls.surfaces = json.loads(SURFACES.read_text())
        cls.matrix = MATRIX.read_text()

    def test_fixture_has_distinct_a_b_c_and_block_record(self):
        fixture = self.observations["fixture"]
        self.assertIn("block", fixture)
        self.assertNotEqual(fixture["A1"].split("/")[2], fixture["B1"].split("/")[2])
        self.assertIn("AR", fixture)
        self.assertIn("BR", fixture)
        self.assertIn("A_quote_B", fixture)
        self.assertIn("B_quote_A", fixture)

    def test_thread_presentation_keeps_public_records_for_c(self):
        threads = self.observations["threads"]
        for name in ("AR", "BR", "BR2", "AR2"):
            c_items = threads[name]["carla.test"]["items"]
            self.assertEqual(threads[name]["carla.test"]["status"], 200)
            self.assertTrue(c_items)
            self.assertTrue(all(item["type"].endswith("#postView") for item in c_items))

    def test_all_viewers_are_recorded_without_inferred_policy(self):
        for name, thread in self.observations["threads"].items():
            self.assertIn("alice.test", thread)
            self.assertIn("bob.test", thread)
            self.assertIn("carla.test", thread)
            self.assertIn("anonymous", thread)
            self.assertIn("status", thread["alice.test"])
        self.assertIn("Historical read-provider behavior", self.matrix)
        self.assertIn("Target fork behavior", self.matrix)

    def test_author_feeds_and_search_do_not_collateral_suppress_c(self):
        c = self.surfaces["carla.test"]
        self.assertIn(self.observations["fixture"]["A1"], c["alice.test"])
        self.assertIn(self.observations["fixture"]["B1"], c["bob.test"])
        self.assertIn(self.observations["fixture"]["A_quote_B"], c["search:quotes"])
        self.assertIn(self.observations["fixture"]["B_quote_A"], c["search:quotes"])

    def test_direct_interaction_probe_is_separate_from_presentation(self):
        probes = self.observations["directInteractionProbes"]
        self.assertEqual(probes["pds_create_B_reply_after_block"], "accepted")
        self.assertEqual(probes["pds_create_B_mention_after_block"], "accepted")
        self.assertEqual(probes["pds_create_B_follow_A_after_block"], "accepted")
        self.assertIn(
            "no B-originated direct notification",
            probes["appview_notifications_after_probes"]["A"],
        )
        self.assertIn(
            "no A-originated direct notification",
            probes["appview_notifications_after_probes"]["B"],
        )

    def test_matrix_records_reference_and_no_patch_decision(self):
        self.assertIn("Current Bluesky-reference behavior", self.matrix)
        self.assertIn("No collateral third-party suppression was observed", self.matrix)
        self.assertIn("no production presentation patch is justified", self.matrix)


if __name__ == "__main__":
    unittest.main()
