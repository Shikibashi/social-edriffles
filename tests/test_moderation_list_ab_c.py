import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ModerationListAbcTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(
            (ROOT / "tests/fixtures/moderation-list-ab-c.json").read_text()
        )
        cls.report = (ROOT / "docs/RADLIB_CODEX_ACCEPTANCE_REVIEW.md").read_text()

    def test_directional_scenarios_and_classification_vocabulary_exist(self):
        names = {scenario["name"] for scenario in self.fixture["scenarios"]}
        self.assertIn("A direct-blocks B", names)
        self.assertIn("A legacy-listblock contains B", names)
        self.assertIn("remote B listblocks A", names)
        self.assertIn("C views B", names)
        for value in self.fixture["classificationVocabulary"]:
            if value == "INDEPENDENT-THIRD-PARTY":
                self.assertIn("independent", self.report.lower())
            elif value == "LOCAL ATTENTION FILTER":
                self.assertIn("attention", self.report.lower())
            else:
                self.assertIn(value, self.report)

    def test_report_does_not_turn_c_into_a_blocker(self):
        self.assertIn("Charlie", self.report)
        self.assertIn("independent", self.report.lower())
        self.assertIn("listblock", self.report.lower())
        self.assertIn("inert", self.report.lower())


if __name__ == "__main__":
    unittest.main()
