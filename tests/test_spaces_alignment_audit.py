import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SpacesAlignmentAuditTests(unittest.TestCase):
    def test_audit_artifacts_are_present_and_alpha_boundary_is_explicit(self):
        audit = (ROOT / 'docs/SPACES_ALIGNMENT_AUDIT.md').read_text()
        authority = (ROOT / 'docs/SPACES_AUTHORITY_MODEL.md').read_text()
        acceptance = (ROOT / 'docs/SPACES_ALIGNMENT_ACCEPTANCE.md').read_text()

        self.assertIn('ALPHA-GATED / OWNER ACCEPTANCE PENDING', audit)
        self.assertIn('Protected block', audit)
        self.assertIn('two-PDS', audit)
        self.assertIn('Radlib is policy/control only', audit)
        self.assertIn('## Multi-writer community read', authority)
        self.assertIn('not end-to-end encryption', authority)
        self.assertIn('ALPHA-GATED / OWNER ACCEPTANCE PENDING', acceptance)
        self.assertIn('A9', acceptance)
        self.assertIn('A12', acceptance)

    def test_audit_does_not_promote_browser_or_contract_checks_to_e2e(self):
        acceptance = (ROOT / 'docs/SPACES_ALIGNMENT_ACCEPTANCE.md').read_text()
        self.assertIn('does not authorize production use', acceptance)
        self.assertIn('A15', acceptance)


if __name__ == '__main__':
    unittest.main()
