# ShopSafe — deliberately insecure local test website

**This is an educational test fixture for Sentinel AI, not a real store.** It includes intentionally planted security mistakes with 100% fictional customer data. **Run only on your own machine.** The web server binds to `127.0.0.1`, not a public interface.

## Quick start

Requires Python 3.9+; **no pip installs**.

```bash
python3 server.py
```

Visit **http://127.0.0.1:8765**. The storefront includes products and an interactive order lookup for fictional users Alice and Bob.

### See the three planted findings

1. **Public fake key** in `public/app.js`: the value beginning `sk_test_SHOPSAFE_FAKE_` is deliberately *not* a real credential. Your source-code scanner should flag the pattern but label it a potential finding until validated.
2. **Missing ownership check** in `server.py`: try viewer **Alice** with order **#1002 — Bob** in the page's "Track an order" form. Vulnerable mode returns Bob's fictional order instead of blocking access. This is a local BOLA/IDOR training case.
3. **Missing CSP header** on HTTP responses in `server.py`: a simple header check can confirm it is absent. A missing header is defense-in-depth, not proof of a working XSS attack.

You can compare your agents' results with `fixtures/expected-findings.json`. **Do not hardcode these expected findings into your scanner.**

## Demo: compare vulnerable and fixed modes

**Terminal 1 — vulnerable:**
```bash
python3 server.py
```

**Terminal 2 — tests:**
```bash
python3 -m unittest discover -s tests -v
```

Stop the server with Ctrl+C, then restart in fixed mode:

```bash
FIXED_MODE=1 python3 server.py
```

Re-run tests. Fixed mode blocks cross-account orders and adds a basic CSP. The fake secret marker stays in `public/app.js` on purpose so you can test partial remediation; delete its line manually to resolve that last finding. In a real application, the `viewer` query parameter is **not authentication**, so this fixed mode illustrates ownership-check logic, not a production-quality security solution.

## Connecting Sentinel

Choose one of two supported approaches:

- **Repository analysis:** point the scanners at this extracted directory and analyze `public/app.js` and `server.py` as text. **Do not execute arbitrary repositories from users.**
- **Local URL inspection:** call `http://127.0.0.1:8765`, view `/app.js`, check response headers, and exercise the documented *local, fictional* order fixture. Remote Gemini services cannot access your laptop's localhost; collect evidence locally in your backend, redact as needed, then send structured findings to Gemini.

Suggested demo flow: start ShopSafe → scan with Sentinel → show three grounded findings → explain with Gemini → show suggested repairs → restart with `FIXED_MODE=1` → rescan → remove fake-key line and rescan again.

## Safety notes

- All credentials are fabricated and cannot access third-party services.
- No real names, passwords, accounts, transactions, or payment processing.
- No offensive scanner, remote brute force, or exploit automation is included.
- Only test systems you own or are authorized to assess.
- This repository is a **harness for measuring Sentinel**, not itself the hackathon submission.
