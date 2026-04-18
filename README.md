# QAFlow — Test Suite

Automated tests for web app: Desktop (UI/API/E2E) + Mobile (Pixel 5 / iPhone 13).

## Stack

- Python 3.9+ · pytest · Playwright · Allure

## Structure

```
tests/
├── desktop/
│   ├── api/      # JSONPlaceholder
│   ├── ui/       # SauceDemo, the-internet
│   └── e2e/      # Full flows
└── mobile/       # Pixel 5 + iPhone 13 emulation
```

## Run

```bash
pip install -r requirements.txt
playwright install chromium

make test-api        # API tests
make test-ui         # UI tests
make test-e2e        # E2E tests
make test-mobile     # Mobile tests
make test-all        # Everything

make report          # Open Allure report
```

## CI

GitHub Actions — `.github/workflows/tests.yml`  
Triggers: `workflow_dispatch` → choose suite (all / ui / api / e2e / mobile)  
Report: deployed to GitHub Pages after each run.
