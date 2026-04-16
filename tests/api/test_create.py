import allure
import pytest

pytestmark = pytest.mark.api


@allure.title("POST /posts — создание поста")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_post(session, jsonplaceholder):
    payload = {"title": "QA Bot", "body": "test post", "userId": 1}

    with allure.step("POST /posts"):
        r = session.post(f"{jsonplaceholder}/posts", json=payload)

    with allure.step("Статус 201"):
        assert r.status_code == 201

    with allure.step("id и title в ответе"):
        body = r.json()
        assert "id" in body
        assert body["title"] == payload["title"]
        assert body["userId"] == payload["userId"]


@allure.title("PUT /posts/1 — полное обновление поста")
@allure.severity(allure.severity_level.NORMAL)
def test_update_post(session, jsonplaceholder):
    payload = {"id": 1, "title": "updated", "body": "updated body", "userId": 1}

    with allure.step("PUT /posts/1"):
        r = session.put(f"{jsonplaceholder}/posts/1", json=payload)

    with allure.step("Статус 200 и title обновлён"):
        assert r.status_code == 200
        assert r.json()["title"] == "updated"


@allure.title("DELETE /posts/1 — удаление поста")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_post(session, jsonplaceholder):
    with allure.step("DELETE /posts/1"):
        r = session.delete(f"{jsonplaceholder}/posts/1")

    with allure.step("Статус 200"):
        assert r.status_code == 200


@allure.title("GET /posts?userId=1 — фильтрация по userId")
@allure.severity(allure.severity_level.NORMAL)
def test_filter_posts_by_user(session, jsonplaceholder):
    with allure.step("GET /posts?userId=1"):
        r = session.get(f"{jsonplaceholder}/posts", params={"userId": 1})

    with allure.step("Статус 200"):
        assert r.status_code == 200

    with allure.step("Все посты принадлежат userId=1"):
        posts = r.json()
        assert len(posts) > 0
        assert all(p["userId"] == 1 for p in posts)
