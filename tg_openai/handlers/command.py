from aiogram import types
from loader import dp

from tg_openai.utils.notify_admins import BotAdministration


class CommandHandler:
    @staticmethod
    @dp.message_handler(text='/start')
    async def command_start(message: types.Message):
        await message.answer(
            f'Привет {message.from_user.full_name}!\nМой функционал можно '
            'вызвать специальными командами. \nДля обычного общения с ChatGPT '
            'просто задай любой интересующий тебя вопрос. К примеру: "Ты '
            'работаешь?"\nТак же я могу генерировать различные изображения. '
            'Для этого напиши ключевое слово "Изображение", и укажите кол-во '
            'изображений. Дальше опишите что вы хотите. К примеру: '
            '"Изображение снега, 5", бот сгенерирует для вас изображение в '
            'кол-ве 5ти штук.'
        )

    @staticmethod
    @dp.message_handler(text='/help')
    async def command_help(message: types.Message):
        await message.answer(
            "Если у тебя возникли проблемы, напиши команду '/need_help', и "
            "напишите свой телеграмм аккаунт (Пример @ru_gpt_bot). Скоро тебе "
            "ответят специалисты"
        )

    @staticmethod
    @dp.message_handler(text='/need_help')
    async def command_help_user(message: types.Message):
        if message.from_user.username:
            await message.answer(
                "Заявка на помощь была зарегистрирована. В скором времени с "
                "тобой свяжутся."
            )
            await BotAdministration.help_user(dp, message.from_user.username)
        else:
            await message.answer(
                "Для регистрации заявки, укажите свою имя в настройках "
                "телеграмма."
            )
