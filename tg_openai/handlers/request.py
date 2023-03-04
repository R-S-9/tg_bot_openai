import datetime

from loguru import logger
from aiogram import types
from dotenv import load_dotenv

from loader import dp, bot
from tg_openai.utils.request_verification import RequestVerification
from tg_openai.utils.request_limit import RequestLimited

from db.sqlite_base import SQLConnect


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

        if not SQLConnect().user_exists(message.from_user.username):
            if await RequestLimited().check_user(message) is False:
                return
        await message.answer("Обрабатываю ваш запрос!")

        try:
            response, is_image = await RequestVerification. \
                checking_for_type_request(
                    message.text, message.from_user.username
                )

            print(
                'Запрос '
                f'{message.from_user.username}, {datetime.datetime.now()}'
            )

            number_request = SQLConnect().get_number_request_by_user_name(
                message.from_user.username
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
                    f'Запрос №{number_request}\n\n'
                    f'{response}\n\n[ChatGPTRuBot Подписаться]'
                    '(https://t.me/ru_gpt_bot)',
                    parse_mode='Markdown'
                )
        except Exception as _ex:
            logger.error(
                f'Запрос от {message.from_user.username} получил ошибку,'
                f' вопрос: {message.text}, ошибка:{_ex}'
            )
            await message.answer(
                f'Ошибка! {_ex}'
            )
