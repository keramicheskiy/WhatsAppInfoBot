import requests

import services
from config import admins
from services import get_settings
import config


def admins_only_or_send_base_message(func):
    def wrapper(notification, *args, **kwargs):
        if notification.chat in admins:
            func(notification, *args, **kwargs)
        else:
            number = services.normalize_number(notification.chat)
            print(number, services.get_settings()["ignore"])
            if number not in services.get_settings()["ignore"]:
                notification.answer(get_settings()["base_message"])

    return wrapper


def personal_chats_only(func):
    def wrapper(notification, *args, **kwargs):
        if notification.chat.endswith("@c.us"):
            func(notification, *args, **kwargs)

    return wrapper


def redirect(func):
    def wrapper(notification, *args, **kwargs):
        number = services.normalize_number(notification.chat)
        redirects = services.get_settings()["redirect"]
        if number in redirects.keys():
            text = (services.get_settings()["telegram_notification"]
                    .format(redirects[number], notification.message_text))

            url = f"https://api.telegram.org/bot{config.telegram_token}/sendMessage"
            data = {"chat_id": config.admin_tg_id, "text": text}
            requests.post(url, data)
        func(notification, *args, **kwargs)

    return wrapper
