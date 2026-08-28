import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SOCIAL = ROOT / "upstream/social-app/src"
PDS = ROOT / "upstream/atproto-pds/packages/pds/src"


class ServiceAuthCurrentStateTests(unittest.TestCase):
    def test_social_app_separates_appview_and_pds_clients(self):
        clients = (SOCIAL / "state/session/clients.ts").read_text()
        self.assertIn("getServiceAuth", clients)
        self.assertIn("authorization", clients)
        self.assertIn("return createLexClient(agent, {appLabelers: null})", clients)
        self.assertIn("service: CHAT_PROXY_SERVICE", clients)

    def test_social_app_proxy_identity_is_configuration_not_authentication(self):
        constants = (SOCIAL / "lib/constants.ts").read_text()
        env = (SOCIAL / "env/common.ts").read_text()
        self.assertIn("BLUESKY_PROXY_HEADER", constants)
        self.assertIn("APPVIEW_PROXY_SERVICE", constants)
        self.assertIn("EXPO_PUBLIC_APPVIEW_SERVICE_DID", env)
        self.assertIn("did:example:unconfigured-appview", env)
        self.assertNotIn("did:web:api.bsky.app", env)

    def test_first_party_pds_mints_service_auth_for_selected_read_services(self):
        service_auth = (PDS / "api/com/atproto/server/getServiceAuth.ts").read_text()
        context = (PDS / "context.ts").read_text()
        self.assertIn("com.atproto.server.getServiceAuth", service_auth)
        self.assertIn("serviceAuthJwt", context)
        self.assertIn("serviceAuthHeaders", context)

    def test_current_state_is_documented_as_verified(self):
        doc = (ROOT / "docs/SERVICE_AUTH_CURRENT_STATE.md").read_text()
        self.assertIn("verified service-auth JWT", doc)
        self.assertIn("| algorithm | accepted algorithm only |", doc)
        self.assertIn("PDS", doc)
        self.assertIn("selected AppView", doc)


if __name__ == "__main__":
    unittest.main()
