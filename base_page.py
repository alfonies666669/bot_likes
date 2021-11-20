import time
import urllib.request
import re
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from browser_func import Browser


class BasePage(Browser):
    LAST_POST = "//div[@class = 'wall_item']"
    TEXT_LIKE = "//div[@class = 'pi_text']"
    CONTENT_IN_POST = "//div[@class = 'wall_item post_withOneLineReactionsDesign'][1]//div[@class = 'thumbs_map " \
                      "fill']//child::a "
    M_ENTER_BUTTON = "input.button"
    M_LOGIN_PASS_FORM_VK = "//input[@class = 'TextInput__native']"
    CHECK_LOGIN = 'a.button.wide_button.success'

    def __init__(self, url, browser):
        super().__init__(url, browser)

    def enter_vk(self, login, password):
        form = self.browser.find_elements_by_xpath(self.M_LOGIN_PASS_FORM_VK)
        for i in form:
            a = i.get_attribute("type")
            if a == "email":
                i.send_keys(login)
            elif a == "password":
                i.send_keys(password)
        self.browser.find_element_by_css_selector(self.M_ENTER_BUTTON).click()

    def check_login_form(self):
        a = self.browser.find_element_by_css_selector(self.CHECK_LOGIN)
        if a is not None:
            return False
        return True

    def get_last_saved_vk(self):
        last_liked_post = self.browser.find_element_by_xpath(self.LAST_POST)
        href_text = last_liked_post.get_attribute("id")
        post = "https://m.vk.com/" + href_text
        return post

    def save_all_pic(self, total_pic, m_main_pic, path):
        how_all = self.browser.find_element_by_xpath(total_pic).text  # how match all number pics; 1 of XXXX
        s1 = re.sub("[^0-9]", "", how_all)
        s = s1[1:]  # correct number

        for i in range(int(s) + 1):
            try:
                main_pic = self.browser.find_element_by_xpath(m_main_pic)  # main pic
                val = main_pic.get_attribute("src")
                img_url = val
                filename = i
                urllib.request.urlretrieve(img_url, path + str(filename) + ".jpg")
                time.sleep(1)
                ActionChains(self.browser).send_keys(Keys.ARROW_RIGHT).perform()
            except Exception as ex:
                self.browser.execute_script("location.reload()")
                print(ex)
                time.sleep(10)
            continue
