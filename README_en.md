# QAFlow

Test framework for a web application. Covers API, UI, E2E, mobile emulation and integration scenarios.

Runs locally via Makefile or remotely via GitHub Actions — including from a Telegram bot.

---

## How it works

```
workflow_dispatch (all / ui / api / e2e / mobile / integration)
         |
    api_tests ──── integration_tests
         |
    ui_tests ────── mobile_tests
         |
    e2e_tests
         |
    allure_report → GitHub Pages
```

Each job is independent. If API fails — UI and E2E still run (`if: always()`).
Allure collects results from all jobs and publishes a single report.

---

## Structure

```
tests/
├── desktop/
│   ├── api/            # HTTP tests via requests
│   │   ├── test_users.py
│   │   └── test_create.py
│   ├── ui/             # browser tests via Playwright
│   │   ├── pages/      # Page Object Model
│   │   ├── test_login.py
│   │   └── test_basic_ui.py
│   └── e2e/            # end-to-end flows
│       ├── pages/
│       └── test_flow.py
├── mobile/             # Pixel 5 + iPhone 13 emulation
│   ├── pages/
│   ├── test_mobile_login.py
│   ├── test_mobile_navigation.py
│   └── test_mobile_ui.py
└── integration/        # event-driven scenarios
    ├── test_webhooks.py
    └── test_event_flow.py
```

---

## What is tested

### API (`tests/desktop/api`)
Target: jsonplaceholder.typicode.com

- GET /users — status 200, response structure, record count
- GET /users/{id} — field validation (id, email, name)
- GET /users/999 — 404 for non-existent resource
- POST /posts — creation, id present in response
- PUT /posts/1 — update, changed fields validated
- DELETE /posts/1 — status 200, empty body
- GET /posts?userId=1 — filtering, all records belong to userId=1

Coverage: positive, negative, filtering, boundary ids.

---

### UI (`tests/desktop/ui`)
Target: saucedemo.com, the-internet.herokuapp.com

- login with valid credentials → redirect to /inventory
- login with wrong password → error message shown
- login with locked account → specific error message
- empty fields → form validation
- checkbox: toggle state
- dropdown: option selection
- dynamic elements: add and remove

Coverage: positive, negative, UI edge cases.

---

### E2E (`tests/desktop/e2e`)
Target: saucedemo.com, httpbin.org

- full flow: login → add item → cart → checkout → confirmation
- negative login flow: multiple invalid attempts in sequence
- API consistency: structure and fields of all users
- httpbin delay: response arrives within timeout

---

### Mobile (`tests/mobile`)
Devices: Pixel 5 (393px), iPhone 13 (390px)

Each test runs on both devices automatically via `pytest_generate_tests`.

- login: success, wrong password, empty fields, locked user
- navigation: burger menu, go to cart, product sorting
- adaptive UI: viewport width, element visibility, page title

---

### Integration (`tests/integration`)
Target: httpbin.org (webhook endpoint simulation)

Models an event-driven system: event delivery, routing, aggregation, suppression.

**test_webhooks.py** — event delivery and validation:
- POST event → status 200, payload delivered intact
- routing headers (X-Alert-Channel, X-Team, X-Priority) reach the destination
- deduplication — identical events produce identical fingerprint
- suppression — suppressed=true and reason preserved in payload
- aggregation — batch of N events delivered as a single package
- retry — slow consumer responds within timeout (2–8 sec)
- wrong method → 405
- schema — missing required field detected before sending

**test_event_flow.py** — chains and routing:
- full chain: source → router (enrichment) → channel (delivery)
- routing by severity: critical → pagerduty, warning → slack
- lifecycle: fired → acknowledged → resolved, each transition delivered
- multi-channel fan-out: one event delivered to two channels

Coverage: positive, negative, edge cases, routing logic, state transitions.

---

## Run

```bash
pip install -r requirements.txt
playwright install chromium

make test-api           # API
make test-ui            # UI
make test-e2e           # E2E
make test-mobile        # Mobile (Pixel 5 + iPhone 13)
make test-mobile-pixel  # Pixel 5 only
make test-mobile-iphone # iPhone 13 only
make test-integration   # Integration
make test-all           # everything

make report             # open Allure in browser
make clean              # remove artifacts
```

---

## Design decisions

**Page Object Model everywhere** — locators and actions live in page classes. Tests only call methods. When a selector changes, you fix it in one place.

**Separate desktop / mobile** — different browser contexts, different fixtures, different viewport configs. Mixing them adds unnecessary complexity.

**`pytest_generate_tests` for devices** — no need to duplicate `@pytest.mark.parametrize` in every test. Devices are injected at the conftest level.

**`if: always()` in CI** — if API fails, UI and E2E still run. Full picture in one pipeline run instead of stopping at the first failure.

**Integration via httpbin** — no real message broker, but event-driven patterns (routing, deduplication, suppression, fan-out) are verified on real HTTP requests. Easy to swap for a real endpoint.

**Screenshot on failure** — via `pytest_runtest_makereport` hook. Automatic, no changes needed in tests. For mobile, the filename includes the device name.

**No time.sleep** — `expect()` everywhere with Playwright's built-in retry.

---

## Limitations

- tests run against public demo sites, not a real product
- no parallel execution (pytest-xdist not connected)
- mobile emulation runs on Chromium — not real Safari on iPhone
- integration tests simulate event-driven system via httpbin, not a real broker
- no run history storage, only the latest Allure report

---
