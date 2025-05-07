import os

from dotenv import load_dotenv

env_file = os.environ.get("ENV_FILE", ".env.local")
load_dotenv(env_file)

id_instance = os.environ.get("ID_INSTANCE")
api_token_instance = os.environ.get("API_TOKEN_INSTANCE")

admins = os.environ.get("ADMINS").split(" ")

telegram_token = os.environ.get("TELEGRAM_TOKEN")
admin_tg_id = os.environ.get("ADMIN_TG_ID")