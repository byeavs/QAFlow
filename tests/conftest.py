import sys
import os

sys.path.insert(0, os.path.dirname(__file__))


def pytest_configure(config):
    config.addinivalue_line("markers", "api: API tests")
    config.addinivalue_line("markers", "ui: UI tests")
    config.addinivalue_line("markers", "e2e: E2E tests")
    config.addinivalue_line("markers", "mobile: Mobile emulation tests")
    config.addinivalue_line("markers", "desktop: Desktop browser tests")
    config.addinivalue_line("markers", "integration: Integration tests (webhooks, event flow)")