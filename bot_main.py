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
    m_page.waiting_complete_load_page()
    m_page.enter_vk(data["m_login_pass_form_vk"], data["login_vk"], data["password_vk"],
                    data["m_enter_button"])
    m_page.waiting_complete_load_page()
    page_likes_vk = BasePage(browser, data["m_likes_page"])
    page_likes_vk.go_to_page()
    window_vk = browser.window_handles[0]
    last_saved_vk = page_likes_vk.get_last_saved_vk()

    inst_page = BasePage(browser, data["link_inst"])
    inst_page.new_tab()
    window_inst = browser.window_handles[1]
    browser.switch_to_window(window_inst)
    inst_page.go_to_page()
    inst_page.waiting_complete_load_page()
    inst_page.enter_inst(data["login_form_inst"], data["pass_form_inst"], data["login_inst"],
                         data["password_inst"], data["enter_button_inst"])
    inst_page.waiting_complete_load_page()
    inst_page.check_save_data(data["save_data"], data["sub_section_save"])
    inst_page.waiting_complete_load_page()
    inst_page.check_save_data(data["note_section"], data["note_submit"])
    inst_page.waiting_complete_load_page()
    page_likes_inst = BasePage(browser, f"https://www.instagram.com/{data['login_inst']}/saved/")
    page_likes_inst.go_to_page()
    page_likes_inst.waiting_complete_load_page()
    last_saved_inst = page_likes_inst.get_last_saved_inst(data["last_pic_inst"])

    while True:
        try:
            time.sleep(10)
            browser.switch_to_window(window_vk)
            browser.refresh()
            page_likes_vk.waiting_complete_load_page()
            new_vk = page_likes_vk.get_last_saved_vk()
            if last_saved_vk != new_vk:
                last_saved_vk = new_vk
                bot.send_message(message.chat.id, text=last_saved_vk)
            browser.switch_to_window(window_inst)
            browser.refresh()
            page_likes_inst.waiting_complete_load_page()
            new_inst = page_likes_inst.get_last_saved_inst(data["last_pic_inst"])
            if last_saved_inst != new_inst:
                last_saved_inst = new_inst
                bot.send_message(message.chat.id, text=last_saved_inst)
            else:
                continue
        except Exception as ex:
            print(ex)
            continue


bot.polling()