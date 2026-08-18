import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CandidateProtocolContractTests(unittest.TestCase):
    def test_replay_fixture_has_required_inputs(self):
        fixture = json.loads((ROOT / 'tests/fixtures/candidate-protocol-replay.json').read_text())
        self.assertEqual(fixture['version'], 1)
        self.assertEqual(fixture['batch']['version'], 1)
        self.assertEqual(fixture['portablePersonalization']['exportLevel'], 'settings')
        self.assertTrue(fixture['hydratedFeatures'])
        self.assertTrue(fixture['ranking']['orderedUris'])

    def test_spec_preserves_frozen_boundaries(self):
        text = (ROOT / 'docs/CANDIDATE_PROTOCOL_V1.md').read_text()
        self.assertIn('Portable Personalization', text)
        self.assertIn('ATTENTION', text.upper())
        self.assertIn('ECDSA P-256/SHA-256', text)
        self.assertIn('anonymous', text)
        self.assertIn('stable-did', text)
        self.assertIn('Candidate Protocol v1', text)


if __name__ == '__main__':
    unittest.main()
