from selenium import webdriver
import time
from base_page import BasePage





def main(browser, link, link_likes, login, password, login_form, pass_form, enter_button, css_saved):
    page_open = BasePage(browser, link)
    page_open.go_to_page()
    if page_open.check_login_user() is False:
        page_open.enter(login, password, login_form, pass_form, enter_button)
    assert page_open.check_login_user()
    page_likes = BasePage(browser, link_likes)
    page_likes.go_to_page()
    last = page_open.get_last_saved(css_saved)
    return last
