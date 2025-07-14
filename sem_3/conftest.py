import pytest, yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

with open("testdata.yaml") as f:
    testdata = yaml.safe_load(f)
    browser_name = testdata["browser"]  # Переименовано для избежания конфликта

@pytest.fixture(scope="function")  # Изменено на function scope
def browser():
    if browser_name == "firefox":
        service = Service(executable_path=GeckoDriverManager().install())
        option = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(service=service, options=option)
    else:
        service = Service(executable_path=ChromeDriverManager().install())
        option = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=option)
    yield driver
    driver.quit()