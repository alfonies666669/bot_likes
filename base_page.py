from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:

    def __init__(self, browser, url, timeout = 10):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def go_to_page(self):
        self.browser.get(self.url)

    def enter(self, login, password, login_form, pass_form, enter_button):
        input1 = self.browser.find_element_by_css_selector(login_form)
        input1.send_keys(login)
        input2 = self.browser.find_element_by_css_selector(pass_form)
        input2.send_keys(password)
        input_button = self.browser.find_element_by_xpath(enter_button)
        input_button.click()

    def enter_tik(self):
        pass

    def check_login_user(self):
        a = self.browser.find_element_by_css_selector('input#index_email.big_text')
        if a is not None:
            return False
        return True

    def get_last_saved(self, css):
        last_like = self.browser.find_element_by_css_selector(css)
        last_like.click()
        url_like = self.browser.current_url
        return url_like

