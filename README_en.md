# QAFlow

Test framework for a web application. Covers API, UI, E2E and mobile emulation.

Runs locally via Makefile or remotely via GitHub Actions — including from a Telegram bot.

---

## How it works

```
workflow_dispatch (all / ui / api / e2e / mobile)
         |
    api_tests
         |
    ui_tests ──── mobile_tests
         |
    e2e_tests
         |
    allure_report → GitHub Pages
```

Each job is independent. If API tests fail — UI and E2E still run (`if: always()`).
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
└── mobile/             # Pixel 5 + iPhone 13 emulation
    ├── pages/
    ├── test_mobile_login.py
    ├── test_mobile_navigation.py
    └── test_mobile_ui.py
```

---

## What is tested

### API (`tests/desktop/api`)
Target: jsonplaceholder.typicode.com

- GET /users — status 200, response structure, record count
- GET /users/{id} — field validation (id, email, name)
- GET /users/999 — 404 for non-existent resource
- POST /posts — creation, id and createdAt present in response
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

## Run

```bash
pip install -r requirements.txt
playwright install chromium

make test-api        # API
make test-ui         # UI
make test-e2e        # E2E
make test-mobile     # Mobile (Pixel 5 + iPhone 13)
make test-all        # everything

make report          # open Allure in browser
make clean           # remove artifacts
```

---

## Design decisions

**Page Object Model everywhere** — locators and actions live in page classes. Tests only call methods. When a selector changes, you fix it in one place.

**Separate desktop / mobile** — different browser contexts, different fixtures, different viewport configs. Mixing them adds unnecessary complexity.

**`pytest_generate_tests` for devices** — no need to duplicate `@pytest.mark.parametrize` in every test. Devices are injected at the conftest level.

**`if: always()` in CI** — if API fails, UI and E2E still run. Full picture in one pipeline run instead of stopping at the first failure.

**Screenshot on failure** — via `pytest_runtest_makereport` hook. Automatic, no changes needed in tests. For mobile, the filename includes the device name.

**No time.sleep** — `expect()` everywhere with Playwright's built-in retry.

---

## Limitations

- tests run against public demo sites, not a real product
- no parallel execution (pytest-xdist not connected)
- mobile emulation runs on Chromium — not real Safari on iPhone
- no run history storage, only the latest Allure report

---
## Report Example

Allure overview after test execution:

<img width="1258" height="678" alt="Снимок экрана — 2026-04-18 в 21 49 36" src="https://github.com/user-attachments/assets/9bd39859-8970-45cc-b745-1b64893cee88" />
