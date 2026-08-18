import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class DailyDriverProductizationTests(unittest.TestCase):
 def test_production_defaults_are_safe(self):
  d=json.loads((ROOT/'tests/fixtures/daily-driver-v1-config.json').read_text()); self.assertFalse(d['production']['localhostDefaults']); self.assertFalse(d['production']['fixtureProviders']); self.assertFalse(d['production']['testCredentials']); self.assertEqual(d['production']['env'],'production')
 def test_docs_use_real_scripts(self):
  t=(ROOT/'docs/BUILDING.md').read_text(); self.assertIn('pnpm build-web',t); self.assertIn('pnpm typecheck:web',t)
  self.assertIn('SIMULATED',(ROOT/'docs/DAILY_DRIVER_V1_FEATURE_MATRIX.md').read_text())
