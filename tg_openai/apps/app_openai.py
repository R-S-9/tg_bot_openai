import os

import openai
from dotenv import load_dotenv


class OpenaiChatBot:
    def __init__(self):
        load_dotenv()

        self.api_key = os.environ.get("API_KEY")
        self.size = "1024x1024"
        self.quantity = 1

    async def request_openai_image(
            self, text: str, size: str, quantity: int
    ):
        openai.api_key = self.api_key

        if not size:
            size = self.size
        if not quantity:
            quantity = self.quantity

        return openai.Image.create(
            prompt=text,
            n=quantity,
            size=size,
        )['data'], True

    async def request_openai_completion(self, text):
        openai.api_key = self.api_key

        return openai.Completion.create(
            model="text-davinci-003",
            prompt=text,
            temperature=0.4,
            max_tokens=1024,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )["choices"][0]["text"], False
