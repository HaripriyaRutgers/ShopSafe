"""Run against a *locally running* ShopSafe service; no third-party targets."""
import json
import os
import unittest
from urllib.request import urlopen
from urllib.error import HTTPError

BASE = os.environ.get('SHOPSAFE_URL', 'http://127.0.0.1:8765')

def request(path):
    try:
        with urlopen(BASE + path, timeout=3) as response:
            return response.status, dict(response.headers), response.read().decode()
    except HTTPError as e:
        return e.code, dict(e.headers), e.read().decode()

class TrainingTargetChecks(unittest.TestCase):
    def test_health(self):
        status, _, body = request('/api/health')
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['app'], 'ShopSafe')

    def test_public_secret_marker(self):
        status, _, body = request('/app.js')
        self.assertEqual(status, 200)
        self.assertIn('sk_test_SHOPSAFE_FAKE_', body)

    def test_cross_account_access(self):
        _, _, health = request('/api/health')
        fixed = json.loads(health)['mode'] == 'fixed'
        status, _, body = request('/api/order?id=1002&viewer=alice')
        if fixed:
            self.assertEqual(status, 403)
        else:
            self.assertEqual(status, 200)
            self.assertEqual(json.loads(body)['owner'], 'bob')

    def test_csp_header(self):
        _, _, health = request('/api/health')
        fixed = json.loads(health)['mode'] == 'fixed'
        _, headers, _ = request('/')
        self.assertEqual('Content-Security-Policy' in headers, fixed)

if __name__ == '__main__':
    unittest.main()
