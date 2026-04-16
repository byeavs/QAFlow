.PHONY: install test-api test-ui test-e2e test-all report clean

install:
	pip install -r requirements.txt
	playwright install chromium

test-api:
	pytest tests/api -m api -v --alluredir=allure-results

test-ui:
	pytest tests/ui -m ui -v --alluredir=allure-results

test-e2e:
	pytest tests/e2e -m e2e -v --alluredir=allure-results

test-all:
	pytest tests/ -v --alluredir=allure-results

report:
	allure serve allure-results

clean:
	rm -rf allure-results allure-report .pytest_cache
