import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SpacesAlphaIntegrationTests(unittest.TestCase):
    def test_pins_record_the_reviewed_spaces_base_and_checkouts(self):
        pins = json.loads((ROOT / 'upstream-pins.json').read_text())
        pds = pins['repositories']['atprotoPds']
        app = pins['repositories']['socialApp']
        self.assertEqual(pds['branch'], 'permissioned-data')
        self.assertEqual(
            pds['commit'], '89deb9fac20e56fa2a262fe9746ed52bc1095ba'
        )
        self.assertEqual(
            pds['checkoutCommit'],
            '5f413a8e50433c685c95c9d7209387a903b1d2f3',
        )
        self.assertEqual(
            app['checkoutCommit'],
            '5a86dcd989d45a62c2586fd421579ee5c9c05eb5',
        )

    def test_documentation_preserves_alpha_and_owner_boundaries(self):
        doc = (ROOT / 'docs/SPACES_ALPHA_INTEGRATION.md').read_text()
        self.assertIn('ALPHA_OPT_IN', doc)
        self.assertIn('PDS_SPACES_ALPHA_ENABLED=true', doc)
        self.assertIn('native Hermes/Metro WebCrypto compatibility', doc)
        self.assertIn('owner acceptance', doc)

    def test_documentation_includes_test_only_reference_pds_docker_lane(self):
        doc = (ROOT / 'docs/SPACES_ALPHA_INTEGRATION.md').read_text()
        self.assertIn(
            'ghcr.io/bluesky-social/atproto:pds-spaces-alpha',
            doc,
        )
        self.assertIn('non-production testing', doc)
        self.assertIn('127.0.0.1:2583:3000', doc)
        self.assertIn('spaces-alpha-test-data', doc)
        self.assertIn('/xrpc/_health', doc)
        self.assertIn('/xrpc/com.atproto.server.describeServer', doc)
        self.assertIn('real accounts must not be migrated', doc)

    def test_client_uses_standard_spaces_namespaces_and_legacy_gate(self):
        client = (ROOT / 'upstream/social-app/src/lib/atproto/spaces/rpc.ts').read_text()
        env = (ROOT / 'upstream/social-app/src/env/common.ts').read_text()
        self.assertIn('com.atproto.space.putRecord', client)
        self.assertIn('com.atproto.space.getSpaceCredential', client)
        self.assertIn('com.atproto.space.getRepo', client)
        self.assertIn('com.atproto.space.listRepoOps', client)
        self.assertIn('com.atproto.space.getBlob', client)
        feed = (
            ROOT / 'upstream/social-app/src/state/queries/private-feed.ts'
        ).read_text()
        self.assertIn('createSpaceCredentialClient', feed)
        self.assertIn('repo: authorityDid', feed)
        credential = (
            ROOT / 'upstream/social-app/src/lib/atproto/spaces/credential.ts'
        ).read_text()
        self.assertIn("'DPoP' : 'Bearer'", credential)
        self.assertIn('ath', credential)
        self.assertIn('EXPO_PUBLIC_SPACES_ALPHA_ENABLED', env)
        self.assertIn('EXPO_PUBLIC_LEGACY_RADLIB_PRIVATE_ENABLED', env)


if __name__ == '__main__':
    unittest.main()
