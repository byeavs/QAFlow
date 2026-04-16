import pytest
import requests


@pytest.fixture(scope="session")
def reqres():
    return "https://reqres.in/api"


@pytest.fixture(scope="session")
def jsonplaceholder():
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    yield s
    s.close()
