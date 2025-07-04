import requests


def test_existing_post(login, data):
    """Проверка получения существующих постов"""
    headers = {"X-Auth-Token": login}
    response = requests.get(
        data["address"] + "api/posts",
        params={"owner": "notMe"},
        headers=headers
    )
    assert response.status_code == 200, "Ошибка получения постов"

    posts = response.json().get("data", [])
    assert len(posts) > 0, "Нет ни одного поста для отображения"


def test_create_post(login, unique_post_data, data):
    """Проверка создания нового поста"""
    headers = {"X-Auth-Token": login}
    response = requests.post(
        data["address"] + "api/posts",
        headers=headers,
        data=unique_post_data
    )
    assert response.status_code == 200, "Ошибка создания поста"
    assert "id" in response.json(), "ID поста не возвращен в ответе"


def test_created_post_exists(login, created_post, data):
    """Проверка наличия созданного поста по описанию"""
    headers = {"X-Auth-Token": login}
    response = requests.get(
        data["address"] + "api/posts",
        params={"owner": "me"},
        headers=headers
    )
    assert response.status_code == 200, "Ошибка получения постов"

    posts = response.json().get("data", [])
    descriptions = [post["description"] for post in posts]
    assert created_post["description"] in descriptions, "Созданный пост не найден"