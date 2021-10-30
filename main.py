from selenium import webdriver
import time
from base_page import BasePage


def vk():
    link = "https://vk.com/"
    link_likes = "https://vk.com/feed?section=likes"
    css_saved = "div.wall_text"
    login = "+79961650920"
    password = "22021996Alexandr)"
    login_form = 'input#email.big_text'
    pass_form = 'input#pass.big_text'
    enter_button = "//*[@id='login_button']"


def inst():
    login = "santscho6666"
    password = "22021996alexandruser1234"
    link = "https://www.instagram.com/"
    link_likes = f"https://www.instagram.com/{login}/saved/"
    css_saved = ''
    login_form = "//input[@name='username']"
    pass_form = "//input[@name='password']"
    enter_button = "button[type='submit']"


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
