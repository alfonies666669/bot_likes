import json
import time
from base_page import BasePage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():

    options = Options()
    options.headless = True
    options.add_experimental_option('prefs', {'intl.accept_languages': "ru"})
    browser = webdriver.Chrome(options=options)

    config_path = "data.json"
    config_file = open(config_path)
    data = json.load(config_file)

    page_open = BasePage(browser, data["link_vk"])
    page_open.go_to_page()
    if page_open.check_login_user() is False:
        page_open.enter(data["login_vk"], data["password_vk"], data["login_form_vk"], data["pass_form_vk"],
                        data["enter_button_vk"])
    time.sleep(3)
    page_likes = BasePage(browser, data["link_likes_vk"])
    page_likes.go_to_page()
    last = page_open.get_last_saved(data["css_saved_vk"])
    print(last)
    time.sleep(5)
    browser.close()
    browser.quit()


if __name__ == "__main__":
    main()
