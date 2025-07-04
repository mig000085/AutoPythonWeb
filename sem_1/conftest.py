import pytest
import yaml
import requests
import time
import uuid

# Загрузка конфигурации
with open("config.yaml") as f:
    config_data = yaml.safe_load(f)

@pytest.fixture(scope="session")
def data():
    """Фикстура с данными конфигурации"""
    return config_data

@pytest.fixture(scope="session")
def login(data):
    """Фикстура для получения токена авторизации"""
    response = requests.post(
        data["address"] + "gateway/login",
        data={"username": data["username"], "password": data["password"]}
    )
    token = response.json().get("token")
    if not token:
        pytest.fail("Ошибка авторизации: токен не получен")
    return token

@pytest.fixture
def unique_post_data():
    """Генерация уникальных данных для поста"""
    timestamp = int(time.time())
    unique_id = uuid.uuid4().hex[:8]
    return {
        "title": f"Заголовок {unique_id}",
        "description": f"Описание {timestamp}",
        "content": f"Контент {unique_id}-{timestamp}"
    }

@pytest.fixture
def created_post(login, unique_post_data, data):
    """Фикстура создания поста и возврата его данных"""
    headers = {"X-Auth-Token": login}
    response = requests.post(
        data["address"] + "api/posts",
        headers=headers,
        data=unique_post_data
    )
    if response.status_code != 200:
        pytest.fail(f"Ошибка создания поста: {response.status_code}")
    return unique_post_data