import os
from typing import Any

import openai
from dotenv import load_dotenv

from tg_openai.db.sqlite_base import SQLConnect


class OpenaiChatBot:
    def __init__(self):
        load_dotenv()

        self.api_key = os.environ.get("API_KEY")
        self.size = os.environ.get('IMAGE_SIZE')
        self.quantity = os.environ.get('IMAGE_QUANTITY')

    async def request_openai_image(
            self, text: str, size: str, quantity: int, username: str
    ) -> tuple[Any, bool]:
        """Create image"""
        try:
            if not size:
                size = self.size
            if not quantity:
                quantity = self.quantity

            openai.api_key = SQLConnect().get_token_by_user_name(username)

            return openai.Image.create(
                prompt=text,
                n=quantity,
                size=size,
            )['data'], True
        except Exception as _ex:
            print(_ex)
        return "", True

    @staticmethod
    async def request_openai_completion(
            text: str, username: str
    ) -> tuple[Any, bool]:
        """Create openai text"""

        try:
            openai.api_key = SQLConnect().get_token_by_user_name(username)

            return openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": text
                    }
                ]
            )["choices"][0]["message"]["content"], False
        except Exception as _ex:
            print(_ex)
        return "", False
