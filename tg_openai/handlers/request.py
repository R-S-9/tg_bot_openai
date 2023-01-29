import datetime

from loguru import logger
from aiogram import types
from dotenv import load_dotenv

from loader import dp, bot
from tg_openai.utils.request_verification import RequestVerification


logger.add(
    "logs/tg_bot.log",
    format="{time} {level} {message}",
    level="INFO",
    rotation="10MB",
    compression="zip"
)

load_dotenv()
number_request = 0


class RequestAPI:
    @staticmethod
    @dp.message_handler()
    async def handle_text(message: types.Message):
        global number_request
        number_request += 1

        try:
            response, is_image = await RequestVerification.\
                checking_for_type_request(
                    message.text
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
