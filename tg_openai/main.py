from aiogram import executor, Dispatcher

from handlers import dp
from utils.notify_admins import BotAdministration
from utils.set_bot_commands import set_default_commands

from db.sqlite_base import SQLConnect


async def bot_on_startup(disp: Dispatcher):
    await BotAdministration.on_startup_notify(disp)
    await set_default_commands(disp)

    print('Bot is running')


if __name__ == '__main__':
    # Отображение информации о БД
    SQLConnect().db_information()

    # Создание таблицы User
    SQLConnect().create_user_table()

    # Создание таблицы Token
    SQLConnect().create_key_table()

    executor.start_polling(dp, on_startup=bot_on_startup)

    # Закрытие бд
    SQLConnect().close_sql_connection()
