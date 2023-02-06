import re

from tg_openai.apps.app_openai import OpenaiChatBot


class RequestVerification:
    @staticmethod
    async def checking_for_type_request(text: str, api_key: str or None):
        """
            Если в запросе есть слово 'Изображение', то вызывается
            функция где, генерируется изображения
        """
        # TODO добавить разрешение в запрос

        text = text.lower()

        if re.search(r'^изображени\w', text) or \
                re.search(r'^\d изображени\w', text):

            if re.search(r',', text[:14]):
                list_text = text.split(r', ')
            else:
                list_text = [
                    text[:14], text[14:]
                ]
            try:
                quantity = re.findall('[0-9]', list_text[0])

                if re.findall('[0-9]', list_text[0]) and api_key:
                    quantity = int(quantity[0])
                else:
                    quantity = 1
            except Exception:
                quantity = 1
            return await OpenaiChatBot().request_openai_image(
                f"Изображение {' '.join(list_text[1:])}",
                "1024x1024",
                quantity,
                api_key,
            )
        return await OpenaiChatBot().request_openai_completion(
            text, api_key
        )
