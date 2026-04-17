import allure
import pytest

pytestmark = pytest.mark.api

BASE = "https://jsonplaceholder.typicode.com"


@allure.title("GET /users — статус 200 и непустой список")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_users(session, jsonplaceholder):
    with allure.step("GET /users"):
        r = session.get(f"{jsonplaceholder}/users")

    with allure.step("Статус 200"):
        assert r.status_code == 200

    with allure.step("Список непустой, 10 пользователей"):
        users = r.json()
        assert isinstance(users, list)
        assert len(users) == 10


@allure.title("GET /users/1 — валидация полей пользователя")
@allure.severity(allure.severity_level.NORMAL)
def test_get_single_user(session, jsonplaceholder):
    with allure.step("GET /users/1"):
        r = session.get(f"{jsonplaceholder}/users/1")

    with allure.step("Статус 200"):
        assert r.status_code == 200

    with allure.step("Поля id, name, email, username присутствуют"):
        u = r.json()
        assert u["id"] == 1
        assert "@" in u["email"]
        assert u["name"]
        assert u["username"]


@allure.title("GET /users/999 — несуществующий пользователь возвращает 404")
@allure.severity(allure.severity_level.NORMAL)
def test_get_user_not_found(session, jsonplaceholder):
    with allure.step("GET /users/999"):
        r = session.get(f"{jsonplaceholder}/users/999")

    with allure.step("Статус 404"):
        assert r.status_code == 404


@allure.title("GET /posts — 100 постов")
@allure.severity(allure.severity_level.MINOR)
def test_get_posts(session, jsonplaceholder):
    with allure.step("GET /posts"):
        r = session.get(f"{jsonplaceholder}/posts")

    with allure.step("Статус 200 и ровно 100 постов"):
        assert r.status_code == 200
        assert len(r.json()) == 100
