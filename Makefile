.PHONY: install test-api test-ui test-e2e test-mobile test-all report clean

install:
	pip install -r requirements-tests.txt
	playwright install chromium

test-api:
	pytest tests/desktop/api -m api -v --alluredir=allure-results

test-ui:
	pytest tests/desktop/ui -m ui -v --alluredir=allure-results

test-e2e:
	pytest tests/desktop/e2e -m e2e -v --alluredir=allure-results

test-mobile:
	pytest tests/mobile -m mobile -v --alluredir=allure-results

test-mobile-pixel:
	pytest tests/mobile -m mobile -v --alluredir=allure-results -k "Pixel"

test-mobile-iphone:
	pytest tests/mobile -m mobile -v --alluredir=allure-results -k "iPhone"

test-all:
	pytest tests/ -v --alluredir=allure-results

report:
	allure serve allure-results

clean:
	rm -rf allure-results allure-report .pytest_cache
