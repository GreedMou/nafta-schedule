from datetime import datetime
import time
from aiogram import Bot, Dispatcher, types
from bot.misc import parse
from bot.misc import TgKeys
from bot.keyboards import reply

bot = Bot(token=TgKeys.TOKEN, parse_mode='HTML')


def register_user_handlers(dp: Dispatcher):
    # todo: register all user handlers
    dp.register_message_handler(send_date, lambda msg: msg.text in ['Отримати розклад', 'Оновити'])
    dp.register_message_handler(get_schedule, regexp=r'[\d]{2}.[\d]{2}')
    dp.register_message_handler(on_startup, commands='start')
    pass


async def on_startup(msg: types.Message):
    await bot.send_message(msg.from_id, text='Main Menu', reply_markup=reply.get_main_menu())


async def send_date(msg: types.Message):
    await bot.send_message(msg.from_id, text='Date', reply_markup=reply.get_week_menu())


async def get_schedule(msg: types.Message):
    date = datetime.strptime(msg.text, '%d.%m')
    date_now = datetime.now()

    date = date.replace(year=date_now.year)
    timedelta = datetime.now()-date
    offset = timedelta.days

    data = parse.get_schedule(offset)
    text = f'Розклад на {msg.text}:\n\n'

    for key, value in data.items():
        text += f'{key}. {value["subject"]}\n' \
               f'Час: {value["hours"]}\n' \
               f'Викладач: {value["lecturer"]}\n' \
               f'<b>Посилання:</b> {value["url"]}\n\n' \

    await msg.reply(text, parse_mode='HTML')
