from aiogram import Bot, Dispatcher, types

from settings.config import tg_bot_token

bot = Bot(
    token=tg_bot_token, parse_mode=types.ParseMode.HTML
)

dp = Dispatcher(bot)
