import logging
from api_helper import api_get_posts, api_create_post, api_get_user_posts


def test_get_posts(login):
    """Проверка получения существующих постов"""
    logging.info("Test API 1 Starting - Проверка получения постов")
    res = api_get_posts(login)  # или api_get_posts(login, owner="notMe")
    assert res is not None, "Ошибка получения постов - ответ None"
    assert res.status_code == 200, f"Ошибка статус кода: {res.status_code}"

    posts = res.json().get("data", [])
    assert len(posts) > 0, "Нет ни одного поста для отображения"

    # Проверяем, что есть хотя бы один пост с непустым заголовком
    assert any(post.get("title") for post in posts), "Нет постов с заполненным заголовком"


def test_create_post(login, post_data):
    """Проверка создания нового поста"""
    logging.info("Test API 2 Starting - Проверка создания поста")
    res = api_create_post(login, post_data)
    assert res is not None, "Ошибка создания поста - ответ None"
    assert res.status_code == 200, f"Ошибка статус кода: {res.status_code}"
    assert "id" in res.json(), "ID поста не возвращен в ответе"


def test_get_user_posts(login, created_post):
    """Проверка наличия созданного поста"""
    logging.info("Test API 3 Starting - Проверка постов пользователя")
    res = api_get_user_posts(login)
    assert res is not None, "Ошибка получения постов - ответ None"
    assert res.status_code == 200, f"Ошибка статус кода: {res.status_code}"

    posts = res.json().get("data", [])
    descriptions = [post["description"] for post in posts]
    assert created_post["description"] in descriptions, "Созданный пост не найден"