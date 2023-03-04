import re

from tg_openai.apps.app_openai import OpenaiChatBot


class RequestVerification:
    @staticmethod
    async def checking_for_type_request(text: str, user_name: str):
        """
            Если в запросе есть слово 'Изображение', то вызывается
            функция где, генерируется изображения
        """

        text = text.lower()

        if re.search(r'^изображени\w', text):
            return await OpenaiChatBot().request_openai_image(
                text,
                '512x512',  # "1024x1024",
                1,
                user_name,
            )
        return await OpenaiChatBot.request_openai_completion(
            text, user_name
        )
