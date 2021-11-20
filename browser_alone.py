from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverFactory(object):
    instance = None

    def __new__(cls):
        if cls.instance is None:
            i = object.__new__(cls)
            cls.instance = i
            options = Options()
            options.headless = False
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_experimental_option('prefs', {'intl.accept_languages': 'ru'})
            cls.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        else:
            i = cls.instance
        return i
