import os
import unittest
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

class LiveAppViewLiteTests(unittest.TestCase):
    """Probe a running pinned AppViewLite instance when APPVIEWLITE_URL is set."""

    @unittest.skipUnless(os.getenv('APPVIEWLITE_URL'), 'set APPVIEWLITE_URL for live endpoint checks')
    def test_root_endpoint_serves(self):
        opener = build_opener(NoRedirect)
        request = Request(os.environ['APPVIEWLITE_URL'], method='GET')
        try:
            response = opener.open(request, timeout=10)
        except HTTPError as error:
            self.assertIn(error.code, {301, 302, 307, 308})
        else:
            self.assertEqual(response.status, 200)

    @unittest.skipUnless(os.getenv('APPVIEWLITE_URL'), 'set APPVIEWLITE_URL for live endpoint checks')
    def test_describe_server_endpoint(self):
        base = os.environ['APPVIEWLITE_URL'].rstrip('/')
        request = Request(f'{base}/xrpc/com.atproto.server.describeServer', method='GET')
        with opener().open(request, timeout=10) as response:
            self.assertEqual(response.status, 200)

def opener():
    return build_opener(NoRedirect)

if __name__ == '__main__':
    unittest.main()
