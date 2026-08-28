import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def test_validator(self):
        result = subprocess.run(
            [sys.executable, "scripts/validate_contract.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_three_account_matrix_has_every_viewer(self):
        data = json.loads((ROOT / "tests/fixtures/blocking-matrix.json").read_text())
        viewers = {row["viewer"] for row in data["rows"]}
        self.assertEqual(viewers, {"A", "B", "C"})

    def test_feed_contract_separates_integrity(self):
        data = json.loads((ROOT / "tests/fixtures/feed-contract.json").read_text())
        integrity = next(case for case in data["cases"] if case["id"] == "integrity")
        self.assertEqual(integrity["integrityMustNot"], "invoke-moderation")


if __name__ == "__main__":
    unittest.main()
