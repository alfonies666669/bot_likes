import time
import urllib.request
import re
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    LAST_POST = "//div[@class = 'wall_item post_withOneLineReactionsDesign'][1]"
    TEXT_LIKE = "//div[@class = 'pi_text']"
    CONTENT_IN_POST = "//div[@class = 'wall_item post_withOneLineReactionsDesign'][1]//div[@class = 'thumbs_map " \
                      "fill']//child::a "

    def __init__(self, browser, url, timeout = 10):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def go_to_page(self):
        self.browser.get(self.url)

    def new_tab(self):
        self.browser.execute_script("window.open();")

    def waiting_complete_load_page(self):
        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete')

    def enter_vk(self, log_pass, login, password, enter_button):
        form = []
        form = self.browser.find_elements_by_xpath(log_pass)
        for i in form:
            a = i.get_attribute("type")
            if a == "email":
                i.send_keys(login)
            elif a == "password":
                i.send_keys(password)
        input_button = self.browser.find_element_by_css_selector(enter_button)
        input_button.click()

    def enter_inst(self, login_form, pass_form, login, password, submit_button):
        log_form = self.browser.find_element_by_xpath(login_form)
        log_form.send_keys(login)
        pas_form = self.browser.find_element_by_xpath(pass_form)
        pas_form.send_keys(password)
        sub_butt = self.browser.find_element_by_css_selector(submit_button)
        sub_butt.click()

    def check_save_data(self, svd_section, sub_button):
        section = self.browser.find_element_by_css_selector(svd_section)
        if section is not None:
            button = self.browser.find_element_by_css_selector(sub_button)
            button.click()
        else:
            pass

    def get_last_saved_inst(self, last_saved):
        mini_pic = self.browser.find_element_by_xpath(last_saved)
        href = mini_pic.get_attribute("srcset")
        return href[0: href.index(" ")]

    def check_login_user(self):
        a = self.browser.find_element_by_css_selector('input#index_email.big_text')
        if a is not None:
            return False
        return True

    def get_last_saved_vk(self):
        last_liked_post = self.browser.find_element_by_xpath(self.LAST_POST)
        href_text = last_liked_post.get_attribute("id")
        post = "https://m.vk.com/" + href_text
        return post

    def scroll_down(self):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def save_all_pic(self, total_pic, m_main_pic, path):
        how_all = self.browser.find_element_by_xpath(total_pic).text  # how match all number pics; 1 of XXXX
        s1 = re.sub("[^0-9]", "", how_all)
        s = s1[1:]  # correct number

        for i in range(int(s) + 1):
            main_pic = self.browser.find_element_by_xpath(m_main_pic)  # main pic
            val = main_pic.get_attribute("src")
            img_url = val
            filename = i
            urllib.request.urlretrieve(img_url, path + str(filename) + ".jpg")
            try:
                time.sleep(1)
                ActionChains(self.browser).send_keys(Keys.ARROW_RIGHT).perform()
            except Exception as ex:
                self.browser.execute_script("location.reload()")
                print(ex)
                time.sleep(10)
            continue