import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DeploymentV1Tests(unittest.TestCase):
    def test_production_config_is_safe(self):
        d = json.loads((ROOT / "tests/fixtures/deployment-v1-config.json").read_text())
        p = d["production"]
        self.assertTrue(p["httpsRequired"])
        self.assertFalse(p["localhost"])
        self.assertFalse(p["fixtureEndpoints"])
        self.assertFalse(p["secretBuildVars"])
        self.assertEqual(d["cache"]["hashedAssets"], "immutable")

    def test_headers_and_routes_exist(self):
        h = (ROOT / "deploy/static-headers").read_text()
        r = (ROOT / "deploy/static-redirects").read_text()
        self.assertIn("Content-Security-Policy", h)
        self.assertIn("Cache-Control: no-cache", h)
        self.assertIn("/index.html", r)
        self.assertIn("frame-ancestors", h)

    def test_manifest_redacts_secrets(self):
        d = json.loads((ROOT / "artifacts/deployment-v1-manifest.json").read_text())
        self.assertFalse(d["secretsIncluded"])
        self.assertEqual(d["deploymentStatus"], "READY-BUT-NOT-EXECUTED")
        self.assertNotIn("token", json.dumps(d).lower())
