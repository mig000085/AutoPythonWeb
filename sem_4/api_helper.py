import logging
import requests
import yaml

with open("./testdata.yaml") as f:
    data = yaml.safe_load(f)

def api_get_posts(login, owner="notMe"):
    """Получение постов с API"""
    header = {"X-Auth-Token": login}
    url = data["address"] + "api/posts"
    params = {"owner": owner}

    try:
        res = requests.get(url, params=params, headers=header, timeout=10)
        res.raise_for_status()  # Генерирует исключение для 4XX/5XX статусов
        logging.debug(
            f"GET запрос к {url} с параметрами: {params} и headers: {header}. Код ответа: {res.status_code}")
        return res
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при GET запросе к {url}: {str(e)}")
        return None

def api_create_post(login, post_data):
    """Создание нового поста через API"""
    header = {"X-Auth-Token": login}
    url = data["address"] + "api/posts"

    try:
        res = requests.post(url, headers=header, data=post_data, timeout=10)
        res.raise_for_status()
        logging.debug(
            f"POST запрос к {url} с headers: {header} и данными: {post_data}. Код ответа: {res.status_code}")
        return res
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при POST запросе к {url}: {str(e)}")
        return None

def api_get_user_posts(login):
    """Получение постов текущего пользователя"""
    header = {"X-Auth-Token": login}
    url = data["address"] + "api/posts"
    params = {"owner": "me"}

    try:
        res = requests.get(url, params=params, headers=header, timeout=10)
        res.raise_for_status()
        logging.debug(
            f"GET запрос к {url} с параметрами: {params} и headers: {header}. Код ответа: {res.status_code}")
        return res
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при GET запросе к {url}: {str(e)}")
        return None