import os
from datetime import timedelta

import redis
from aiogram import types


class RequestLimited:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            db=int(os.getenv("REDIS_DB"))
        )

    @staticmethod
    async def check_user(message: types.Message) -> bool:
        req_lim = RequestLimited()

        if req_lim.request_is_limited(
                f'usr-1-{message.chat.id}', 5, timedelta(minutes=1)
        ) or req_lim.request_is_limited(
            f'usr-2-{message.chat.id}', 10, timedelta(days=1)
        ):
            await message.answer(
                'Превышен лимит запросов за промежуток времени, повторите '
                'позднее или приобретите подписку.\nДля получения информации о'
                ' подписке напишите "/subscription"'
            )
            return False
        return True

    def request_is_limited(
            self, key: str, limit: int, period: timedelta
    ) -> bool:
        print('request_is_limited')
        if self.redis_client.setnx(key, limit):
            self.redis_client.expire(key, int(period.total_seconds()))
        bucket_val = self.redis_client.get(key)

        if bucket_val and int(bucket_val) > 0:
            self.redis_client.decrby(key, 1)
            return False
        return True
