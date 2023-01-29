from aiogram import executor
from aiogram import Dispatcher

from handlers import dp
# from
from utils.notify_admins import BotAdministration
from utils.set_bot_commands import set_default_commands


async def bot_on_startup(disp: Dispatcher):
    await BotAdministration.on_startup_notify(disp)
    await set_default_commands(disp)

    print('Bot is running')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=bot_on_startup)
