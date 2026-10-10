"""ShopSafe training target. LOCAL TESTING ONLY. No real data or credentials."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import json, os

BASE = Path(__file__).resolve().parent
FIXED = os.environ.get('FIXED_MODE', '0') == '1'
ORDERS = {
    '1001': {'id': '1001', 'owner': 'alice', 'item': 'Canvas Sneakers', 'total': 49.00},
    '1002': {'id': '1002', 'owner': 'bob', 'item': 'Studio Headphones', 'total': 79.00},
}

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE / 'public'), **kwargs)

    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        if FIXED:
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'")
        # Training issue #3: Content-Security-Policy omitted when FIXED_MODE=0.
        super().end_headers()

    def do_GET(self):
        route = urlparse(self.path)
        if route.path == '/api/health':
            return self.json_reply({'app': 'ShopSafe', 'mode': 'fixed' if FIXED else 'vulnerable'})
        if route.path == '/api/order':
            query = parse_qs(route.query)
            order_id = query.get('id', [''])[0]
            viewer = query.get('viewer', ['alice'])[0]
            order = ORDERS.get(order_id)
            if order is None:
                return self.json_reply({'error': 'Order not found'}, 404)
            # Training issue #2: In vulnerable mode, missing owner authorization.
            # FIXED mode enforces an owner check, but viewer is still only a demo
            # fixture, NOT a production authentication mechanism.
            if FIXED and viewer != order['owner']:
                return self.json_reply({'error': 'Forbidden'}, 403)
            return self.json_reply(order)
        return super().do_GET()

    def json_reply(self, payload, status=200):
        raw = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8765'))
    print(f'ShopSafe ({"fixed" if FIXED else "vulnerable"}) on http://127.0.0.1:{port}')
    ThreadingHTTPServer(('127.0.0.1', port), Handler).serve_forever()
