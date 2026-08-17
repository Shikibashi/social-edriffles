import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SOCIAL = ROOT / "upstream/social-app/src"
APPVIEW = ROOT / "upstream/AppViewLite/src"


class ServiceAuthCurrentStateTests(unittest.TestCase):
    def test_social_app_separates_appview_and_pds_clients(self):
        clients = (SOCIAL / "state/session/clients.ts").read_text()
        self.assertIn("service: BLUESKY_PROXY_HEADER.get()", clients)
        self.assertIn("return createLexClient(agent, {appLabelers: null})", clients)
        self.assertIn("service: CHAT_PROXY_SERVICE", clients)

    def test_social_app_proxy_identity_is_configuration_not_authentication(self):
        constants = (SOCIAL / "lib/constants.ts").read_text()
        env = (SOCIAL / "env/common.ts").read_text()
        self.assertIn("BLUESKY_PROXY_HEADER", constants)
        self.assertIn("${BLUESKY_PROXY_DID}#bsky_appview", constants)
        self.assertIn("did:web:api.bsky.app", env)

    def test_appview_current_bearer_path_is_unverified(self):
        program = (APPVIEW / "AppViewLite.Web/Program.cs").read_text()
        session = (APPVIEW / "AppViewLite/AppViewLiteSession.cs").read_text()
        self.assertIn("handler.ReadJwtToken(unverifiedJwtToken)", program)
        self.assertIn("new SessionIdWithUnverifiedDid(unverifiedDid, unverifiedJwtToken)", program)
        self.assertIn("PdsSession!.AccessJwt", session)
        self.assertIn("CryptographicOperations.FixedTimeEquals", session)

    def test_service_auth_endpoint_is_not_implemented(self):
        server = (APPVIEW / "AppViewLite.Web/ApiCompat/ComAtprotoServer.cs").read_text()
        self.assertIn("GetServiceAuthAsync", server)
        self.assertIn("throw new NotImplementedException()", server)

    def test_current_state_is_documented_as_blocked(self):
        doc = (ROOT / "docs/SERVICE_AUTH_CURRENT_STATE.md").read_text()
        self.assertIn("JWT signature verified | No", doc)
        self.assertIn("service-auth issuance/verification handshake is not available", doc)
        self.assertIn("security blocker", doc)


if __name__ == "__main__":
    unittest.main()
