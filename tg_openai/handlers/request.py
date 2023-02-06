import datetime
import os

from loguru import logger
from aiogram import types
from dotenv import load_dotenv

from loader import dp, bot
from tg_openai.utils.request_verification import RequestVerification
from tg_openai.utils.request_limit import RequestLimited
from .subscribers import number_request


logger.add(
    "logs/tg_bot.log",
    format="{time} {level} {message}",
    level="INFO",
    rotation="10MB",
    compression="zip"
)

load_dotenv()


class RequestAPI:
    @staticmethod
    @dp.message_handler()
    async def handle_text(message: types.Message):
        """Главный handler"""
        if message.from_user.username in number_request:
            # TODO add DB sqlite3
            openai_api_key = os.environ.get(
                f"API_KEY_{message.from_user.username}"
            )
            number_request[message.from_user.username] += 1
        else:
            limit_false = await RequestLimited().check_user(message)
            if limit_false is False:
                return None
            openai_api_key = None
            number_request['anonymous'] += 1

        try:
            response, is_image = await RequestVerification. \
                checking_for_type_request(
                    message.text, openai_api_key
                )

            print(
                f'Запрос {number_request}, {datetime.datetime.now()}'
            )

            if is_image:
                media = types.MediaGroup()

                for img in response:
                    media.attach_photo(
                        img['url'],
                        f'[Оригинал изображения]({img["url"]})',
                        parse_mode='Markdown'
                    )
                await bot.send_media_group(message.chat.id, media=media)
            else:
                await message.answer(
                    f'Запрос №{number_request[message.from_user.username]}\n'
                    f'{response}\n\n[ChatGPTRuBot Подписаться]'
                    '(https://t.me/ru_gpt_bot)',
                    parse_mode='Markdown'
                )
        except Exception as _ex:
            logger.error(
                f'Запрос №{number_request} получил ошибку, вопрос:'
                f'{message.text}, ошибка:{_ex}'
            )
            await message.answer(
                f'Ошибка! {_ex}'
            )
