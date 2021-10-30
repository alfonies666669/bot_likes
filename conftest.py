import pytest
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def browser():
    browser_name = "chrome"
    user_language = "en"
    if browser_name == "chrome":
        options = Options()
        options.headless = True
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        browser = webdriver.Chrome(options=options)
        pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
    else:
        raise pytest.UsageError("pytest error")
    yield browser
    browser.close()
    browser.quit()