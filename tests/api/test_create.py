import allure
import pytest

pytestmark = pytest.mark.api


@allure.title("POST /users — создание пользователя")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_user(session, reqres):
    payload = {"name": "QA Bot", "job": "tester"}

    with allure.step("POST /users"):
        r = session.post(f"{reqres}/users", json=payload)

    with allure.step("Статус 201"):
        assert r.status_code == 201

    with allure.step("id и createdAt в ответе"):
        body = r.json()
        assert "id" in body
        assert "createdAt" in body
        assert body["name"] == payload["name"]


@allure.title("PUT /users/2 — обновление пользователя")
@allure.severity(allure.severity_level.NORMAL)
def test_update_user(session, reqres):
    payload = {"name": "QA Bot", "job": "senior tester"}

    with allure.step("PUT /users/2"):
        r = session.put(f"{reqres}/users/2", json=payload)

    with allure.step("Статус 200 и updatedAt присутствует"):
        assert r.status_code == 200
        assert "updatedAt" in r.json()


@allure.title("DELETE /users/2 — удаление")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_user(session, reqres):
    with allure.step("DELETE /users/2"):
        r = session.delete(f"{reqres}/users/2")

    with allure.step("Статус 204, тело пустое"):
        assert r.status_code == 204
        assert r.text == ""


@allure.title("POST /register — успешная регистрация")
@allure.severity(allure.severity_level.NORMAL)
def test_register_success(session, reqres):
    payload = {"email": "eve.holt@reqres.in", "password": "pistol"}

    with allure.step("POST /register"):
        r = session.post(f"{reqres}/register", json=payload)

    with allure.step("Статус 200 и token в ответе"):
        assert r.status_code == 200
        assert "token" in r.json()
