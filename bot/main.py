import asyncio
import datetime
import time

from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.filters import register_all_filters
from bot.misc import TgKeys
from bot.handlers import register_all_handlers
from bot.database.models import register_models
from misc import parse

x = ['08:55', '10:25', '11:55', '13:35', '15:05']
TIME = []
bot = Bot(token=TgKeys.TOKEN, parse_mode='HTML')

for t in x:
    now = datetime.datetime.now()
    date = datetime.datetime.strptime(t, '%H:%M')
    TIME.append(now.replace(hour=date.hour, minute=date.minute, second=0))

async def __on_start_up(dp: Dispatcher) -> None:
    register_all_filters(dp)
    register_all_handlers(dp)
    register_models()
    # asyncio.create_task(send_to_group())


async def send_to_group():
    print('Func start')

    while True:
        now = datetime.datetime.now() + datetime.timedelta(minutes=1)
        for t in TIME:
            t.replace(year=now.year, month=now.month)
            if now < t:
                start_time = t
                data = parse.get_schedule()
                break
        else:
            data = parse.get_schedule(1)
            offset = int(list(data.keys())[0])-1
            start_time = now.replace(day=now.day+1, hour=TIME[offset].hour,
                                     minute=TIME[offset].minute)
        search_time = start_time + datetime.timedelta(minutes=5)
        text = f'Через 5 хвилин:\n\n'
        s_t = search_time.strftime('%H:%M')
        for key, value in data.items():
            if s_t in value['hours']:
                text += f'{value["subject"]}\n' \
                        f'Викладач: {value["lecturer"]}\n' \
                        f'<b>Посилання:</b> {value["url"]}\n\n'
                break

        sleep_time = start_time.timestamp() - now.timestamp()
        print(sleep_time)
        await asyncio.sleep(sleep_time)
        await bot.send_message(-1001548001238, text=text, parse_mode='HTML')


def start_bot():
    loop = asyncio.get_event_loop()
    dp = Dispatcher(bot, storage=MemoryStorage(), loop=loop)
    dp.loop.create_task(send_to_group())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
