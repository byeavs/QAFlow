import allure
import pytest

pytestmark = pytest.mark.api


@allure.title("GET /users — статус 200 и непустой список")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_users(session, reqres):
    with allure.step("GET /users page=1"):
        r = session.get(f"{reqres}/users", params={"page": 1})

    with allure.step("Статус 200"):
        assert r.status_code == 200

    with allure.step("data непустой"):
        body = r.json()
        assert "data" in body
        assert len(body["data"]) > 0


@allure.title("GET /users/2 — валидация полей")
@allure.severity(allure.severity_level.NORMAL)
def test_get_single_user(session, reqres):
    with allure.step("GET /users/2"):
        r = session.get(f"{reqres}/users/2")

    with allure.step("Статус 200"):
        assert r.status_code == 200

    with allure.step("Поля id, email, first_name, last_name корректны"):
        u = r.json()["data"]
        assert u["id"] == 2
        assert "@" in u["email"]
        assert u["first_name"]
        assert u["last_name"]


@allure.title("GET /users/999 — несуществующий пользователь")
@allure.severity(allure.severity_level.NORMAL)
def test_get_user_not_found(session, reqres):
    with allure.step("GET /users/999"):
        r = session.get(f"{reqres}/users/999")

    with allure.step("Статус 404"):
        assert r.status_code == 404


@allure.title("GET /posts — JSONPlaceholder 100 постов")
@allure.severity(allure.severity_level.MINOR)
def test_get_posts(session, jsonplaceholder):
    with allure.step("GET /posts"):
        r = session.get(f"{jsonplaceholder}/posts")

    with allure.step("Статус 200 и ровно 100 постов"):
        assert r.status_code == 200
        assert len(r.json()) == 100
