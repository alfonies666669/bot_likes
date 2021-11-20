from selenium.webdriver.support.wait import WebDriverWait
from browser_alone import WebDriverFactory
import pickle


class Browser:

    def __init__(self, url, browser):
        self.url = url
        self.browser = browser

    def go_to_page(self):
        self.browser.get(self.url)

    def save_pickle(self):
        pickle.dump(self.browser.get_cookies(), open('session'), 'wb')

    def load_pickle(self):
        for cookie in pickle.load(open('session', 'rb')):
            self.browser.add_cookie(cookie)

    def new_tab(self):
        self.browser.execute_script("window.open();")

    def current(self):
        return self.browser.current_url

    def scroll_down(self):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def waiting_complete_load_page(self):
        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete')
