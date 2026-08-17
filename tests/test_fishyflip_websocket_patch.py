import pathlib
import unittest
from urllib.parse import urljoin, urlsplit, urlunsplit


ROOT = pathlib.Path(__file__).parents[1]
WEBSOCKET_SOURCES = [
    ROOT / "upstream/FishyFlip/src/FishyFlip/ATWebSocketProtocol.cs",
    ROOT / "upstream/FishyFlip/src/FishyFlip/ATJetStream.cs",
]


def websocket_uri(instance: str, connection: str) -> str:
    parsed = urlsplit(instance)
    scheme = {"http": "ws", "ws": "ws", "https": "wss", "wss": "wss"}[parsed.scheme]
    base = urlunsplit((scheme, parsed.netloc, "", "", ""))
    return urljoin(base + "/", connection)


class FishyFlipWebSocketPatchTests(unittest.TestCase):
    def test_local_http_endpoint_preserves_port(self):
        self.assertEqual(websocket_uri("http://127.0.0.1:2583", "/xrpc/subscribe"), "ws://127.0.0.1:2583/xrpc/subscribe")

    def test_https_endpoint_maps_to_wss(self):
        self.assertEqual(websocket_uri("https://example.com", "/xrpc/subscribe"), "wss://example.com/xrpc/subscribe")

    def test_explicit_ws_and_wss_preserve_port(self):
        self.assertEqual(websocket_uri("ws://host:1234", "/stream"), "ws://host:1234/stream")
        self.assertEqual(websocket_uri("wss://host:1234", "/stream"), "wss://host:1234/stream")

    def test_both_fishyflip_paths_use_scheme_aware_uri_builder(self):
        for source in WEBSOCKET_SOURCES:
            text = source.read_text()
            self.assertIn('"http" or "ws" => "ws"', text)
            self.assertIn('"https" or "wss" => "wss"', text)
            self.assertIn("new UriBuilder(this.instanceUri)", text)
            self.assertNotIn('new Uri($"wss://{this.instanceUri.Host}{connection}")', text)


if __name__ == "__main__":
    unittest.main()
