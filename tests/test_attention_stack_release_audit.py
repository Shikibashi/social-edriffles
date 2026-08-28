import json
import unittest
from pathlib import Path
from typing import Any, cast

from tests.exit.attention_stack_exit_harness import run

ROOT = Path(__file__).resolve().parents[1]


class AttentionStackReleaseAuditTests(unittest.TestCase):
    def test_audit_is_release_ready_after_remediation(self):
        d: dict[str, Any] = cast(
            dict[str, Any],
            json.loads(
                (ROOT / "artifacts/attention-stack-v1-release-audit.json").read_text()
            ),
        )
        self.assertEqual(d["decision"], "ATTENTION_STACK_V1_RELEASE_READY")
        self.assertEqual(d["severity"]["P1"], 0)
        t = (ROOT / "docs/ATTENTION_STACK_V1_RELEASE_AUDIT.md").read_text()
        self.assertIn("ATTENTION_STACK_V1_RELEASE_READY", t)

    def test_exit_harness_restores_preferences_without_credentials(self):
        result: dict[str, Any] = run()
        self.assertTrue(result["preferencesRestored"])
        self.assertFalse(result["credentialsExported"])
