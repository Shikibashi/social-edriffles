import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
OBS = ROOT / "artifacts/live-block-presentation-observations.json"
MATRIX = ROOT / "docs/LIVE_BLOCK_PRESENTATION_MATRIX.md"
CONSTITUTION = ROOT / "docs/ASSOCIATION_CONSTITUTION.md"


class AssociationSafetyBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.observations = json.loads(OBS.read_text())
        cls.matrix = MATRIX.read_text()
        cls.constitution = CONSTITUTION.read_text()

    def test_timeline_is_explicit_and_third_party_visible(self):
        timeline = self.observations["safetyBoundaries"]["timeline"]
        self.assertEqual(timeline["A"]["status"], 200)
        self.assertEqual(timeline["B"]["status"], 200)
        self.assertEqual(timeline["C"]["status"], 200)
        self.assertEqual(timeline["anonymous"]["status"], 500)
        self.assertEqual(timeline["C"]["containsA"], "A timeline boundary post")
        self.assertEqual(timeline["C"]["containsB"], "B timeline boundary post")

    def test_deletion_is_not_resurrected(self):
        deletion = self.observations["safetyBoundaries"]["deletion"]
        for viewer in ("A", "B", "C", "anonymous"):
            self.assertEqual(deletion[viewer]["record"], 404)
            self.assertEqual(deletion[viewer]["thread"], 404)

    def test_service_removal_and_interaction_gates_remain_distinct(self):
        boundaries = self.observations["safetyBoundaries"]
        self.assertEqual(boundaries["recordTakedown"]["appViewRecordStatus"], 500)
        self.assertEqual(boundaries["accountTakedown"]["pdsLoginStatus"], 401)
        self.assertEqual(boundaries["accountTakedown"]["pdsError"], "AccountTakedown")
        self.assertEqual(boundaries["threadgate"]["appViewRepliesForB"], 0)
        self.assertIn("detached", boundaries["postgate"]["finding"])

    def test_listblock_and_permissioned_boundaries_are_explicit(self):
        boundaries = self.observations["safetyBoundaries"]
        self.assertEqual(boundaries["listblock"]["listReadStatus"], 200)
        self.assertEqual(boundaries["listblock"]["listsReadStatus"], 200)
        self.assertEqual(boundaries["permissionedData"]["status"], "untested")

    def test_constitution_freeze_principles_are_documented(self):
        required = [
            "bilateral relationship",
            "Unrelated viewers do not inherit",
            "deletion, takedown, account suspension",
            "canonical durable nonassociation",
            "Continuously delegated block-list mutation is not a normal product primitive",
        ]
        for phrase in required:
            self.assertIn(phrase, self.constitution)
        self.assertIn("Association safety boundaries", self.matrix)

    def test_account_takedown_refreshes_before_presentation(self):
        state = self.observations["safetyBoundaries"]["accountTakedown"]
        self.assertEqual(state["pdsLoginStatus"], 401)
        self.assertEqual(state["pdsError"], "AccountTakedown")
        self.assertEqual(state["appViewAuthorFeedStatus"], 200)
        self.assertEqual(state["appViewAuthorFeedItems"], 0)
        self.assertIn("profile placeholder", state["appViewProfileFinding"])

if __name__ == "__main__":
    unittest.main()
