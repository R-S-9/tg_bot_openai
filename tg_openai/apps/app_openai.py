import os
from typing import Any

import openai
from dotenv import load_dotenv


class OpenaiChatBot:
    def __init__(self):
        load_dotenv()

        self.api_key = os.environ.get("API_KEY")
        self.size = os.environ.get('IMAGE_SIZE')
        self.quantity = os.environ.get('IMAGE_QUANTITY')

    async def request_openai_image(
            self, text: str, size: str, quantity: int, api_key: str
    ) -> tuple[Any, bool]:
        if not size:
            size = self.size
        if not quantity:
            quantity = self.quantity
        if not api_key:
            api_key = self.api_key

        openai.api_key = api_key

        return openai.Image.create(
            prompt=text,
            n=quantity,
            size=size,
        )['data'], True

    async def request_openai_completion(
            self, text: str, api_key: str
    ) -> tuple[Any, bool]:
        if not api_key:
            api_key = self.api_key

        openai.api_key = api_key

        return openai.Completion.create(
            model="text-davinci-003",
            prompt=text,
            temperature=0.4,
            max_tokens=1024,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )["choices"][0]["text"], False
