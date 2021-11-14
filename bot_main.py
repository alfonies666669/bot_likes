import telebot
import time
import json
from base_page import BasePage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

config_path = "data.json"
config_file = open(config_path)
data = json.load(config_file)

bot = telebot.TeleBot(data["token"])


@bot.message_handler(commands=["help"])
def send_message(message):
    bot.reply_to(message, "Hello, when you liked a post, the bot will send yo"
                          "u a message with a link to it.")


@bot.message_handler(commands=["start"])
def send_liked(message):
    options = Options()
    options.headless = True
    options.add_experimental_option('prefs', {'intl.accept_languages': "ru"})
    browser = webdriver.Chrome(options=options)

    m_page = BasePage(browser, data["m_vk_feed"])
    m_page.go_to_page()
    time.sleep(2)
    m_page.enter(data["m_login_pass_form_vk"], data["login_vk"], data["password_vk"],
                 data["m_enter_button"])
    time.sleep(2)
    page_likes = BasePage(browser, data["m_likes_page"])
    page_likes.go_to_page()
    last_saved = page_likes.get_last_saved()
    while True:
        time.sleep(10)
        browser.refresh()
        new = page_likes.get_last_saved()
        if last_saved != new:
            last_saved = new
            bot.reply_to(message, last_saved)
        else:
            continue


bot.polling()
