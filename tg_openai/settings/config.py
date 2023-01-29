import os

from dotenv import load_dotenv


load_dotenv()

tg_bot_token = os.environ.get("TG_BOT")
admins_id = [
    os.environ.get("TG_ADMIN_ID"),
]
