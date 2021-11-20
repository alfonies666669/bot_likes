# -*- coding: utf-8 -*-
import telebot
import time
from selenium.common.exceptions import NoSuchElementException
from config import *
import sys
from base_page import BasePage
from browser_alone import WebDriverFactory

bot = telebot.TeleBot(token)
browser = WebDriverFactory().driver


@bot.message_handler(commands=["help"])
def send_message(message):
    bot.reply_to(message, "Hello, when you liked a post, the bot will send yo"
                          "u a message with a link to it.")


def timer():
    timing = time.time()
    while True:
        if time.time() - timing > 10.0:
            break
        return True


def authorization():
    try:
        m_page = BasePage(m_vk_feed_link, browser)
        m_page.go_to_page()
        m_page.waiting_complete_load_page()
        if m_page.check_login_form() is False:
            try:
                m_page.load_pickle()
                time.sleep(2)
                browser.refresh()
            except FileNotFoundError:
                m_page.enter_vk(login_vk, password_vk)
                m_page.waiting_complete_load_page()
                m_page.save_pickle()
        return True
    except:
        return False


def try_auth():
    for i in range(6):
        try:
            if authorization():
                break
            return True
        except Exception:
            continue
    browser.quit()
    browser.close()


@bot.message_handler(commands=["start"])
def send_liked(message):
    if try_auth() is not True:
        while not timer():
            timer()
        try_auth()

    page_likes_vk = BasePage(m_likes_page_link, browser)
    page_likes_vk.go_to_page()
    page_likes_vk.waiting_complete_load_page()
    try:
        last_saved_vk = page_likes_vk.get_last_saved_vk()
    except NoSuchElementException:
        browser.refresh()
        page_likes_vk.waiting_complete_load_page()
        last_saved_vk = page_likes_vk.get_last_saved_vk()

    while True:
        try:
            browser.refresh()
            page_likes_vk.waiting_complete_load_page()
            new_vk = page_likes_vk.get_last_saved_vk()
            if last_saved_vk != new_vk:
                last_saved_vk = new_vk
                bot.send_message(message.chat.id, text=last_saved_vk)
                if timer():
                    if page_likes_vk.current() != m_likes_page_link:
                        send_liked()
            else:
                continue
        except Exception as ex:
            print(ex)
            continue


bot.polling()
