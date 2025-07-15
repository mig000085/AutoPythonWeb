import pytest, yaml, requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

with open("./testdata.yaml") as f:
    data = yaml.safe_load(f)

browser = data["browser"]

@pytest.fixture(scope="session")
def browser():
    if browser == "firefox":
        service = Service(executable_path=GeckoDriverManager().install())
        option = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(service=service, options=option)
    else:
        service = Service(executable_path=ChromeDriverManager().install())
        option = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=option)
    yield driver
    driver.quit()

@pytest.fixture
def login():
    try:
        res = requests.post(
            data["address"] + "gateway/login",
            data={"username": data["username"], "password": data["password"]},
            timeout=10
        )
        res.raise_for_status()
        return res.json()["token"]
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Ошибка авторизации: {str(e)}")

@pytest.fixture
def testtext1():
    return "Test Post Title3"  # или "Test Post 1" в зависимости от того, какой текст вы хотите проверять

@pytest.fixture
def post_data():
    return {
        "title": data["post_title"],
        "description": data["post_description"],
        "content": data["post_content"]
    }

@pytest.fixture
def created_post(login, post_data):
    try:
        header = {"X-Auth-Token": login}
        res = requests.post(
            data["address"] + "api/posts",
            headers=header,
            data=post_data,
            timeout=10
        )
        res.raise_for_status()
        assert res.status_code == 200
        return post_data
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Ошибка создания тестового поста: {str(e)}")