from datetime import datetime

from loguru import logger
from aiogram import Dispatcher

from settings.config import admins_id


logger.add(
    "logs/tg_notify.log",
    format="{time} {level} {message}",
    level="INFO",
    rotation="10MB",
    compression="zip"
)


class BotAdministration:
    @staticmethod
    async def on_startup_notify(dp: Dispatcher):
        for admin in admins_id:
            try:
                await dp.bot.send_message(
                    chat_id=admin, text='Bot is running'
                )
                logger.info(
                    f'Bot is running {datetime.now()}'
                )
            except Exception as _ex:
                await dp.bot.send_message(
                    chat_id=admin, text=f'Bot not starting, error: {_ex}'
                )
                logger.error(
                    f'Bot not starting, error: {_ex}'
                )

    @staticmethod
    async def help_user(dp: Dispatcher, user_name: str):
        for admin in admins_id:
            try:
                await dp.bot.send_message(
                    chat_id=admin,
                    text=f'Пользователю @{user_name}, нужна помощь.',
                )
                logger.info(
                    f'Заявка на помощь пользователю @{user_name}, '
                    f'дата: {datetime.now()}.'
                )
            except Exception as _ex:
                await dp.bot.send_message(
                    chat_id=admin,
                    text=f'Ошибка регистрации заявки на помощь пользователю: '
                         f'{user_name}.'
                )
                logger.error(
                    'Ошибка регистрации заявки на помощь пользователю: '
                    f'{user_name}, дата: {datetime.now()}.'
                )
