import datetime

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    btn_schedule = KeyboardButton('Отримати розклад')
    main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_schedule)
    return main_menu

def get_week_menu():
    d = datetime.datetime.now()
    menu = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Оновити'))
    for i in range(8):
        x = (d + datetime.timedelta(days=i))
        text = x.strftime("%d.%m")
        menu.add(KeyboardButton(text))
    return menu


