import os

from whatsapp_chatbot_python import GreenAPIBot, Notification
from dotenv import load_dotenv

import services
from config import id_instance, api_token_instance, admins
from decorators import admins_only_or_send_base_message, personal_chats_only, redirect
from services import get_settings

bot = GreenAPIBot(
    id_instance=id_instance, api_token_instance=api_token_instance
)


@bot.router.message(text_message=("/base_message", "base_message"))
@personal_chats_only
def message_handler(notification: Notification) -> None:
    notification.answer(get_settings()["base_message"])


@bot.router.message(text_message=("/settings", "settings"))
@personal_chats_only
@admins_only_or_send_base_message
def echo_handler(notification: Notification) -> None:
    notification.answer(str(services.get_settings()).replace("'", '"'))

@bot.router.message()
@redirect
@personal_chats_only
@admins_only_or_send_base_message
def echo_handler(notification: Notification) -> None:
    message = notification.message_text.replace("'", '"')

    if message.split(" ")[0] in ["/settings", "settings"]:
        services.change_settings(" ".join(message.split(" ")[1:]))
        notification.answer(str(services.get_settings()).replace("'", '"'))
    elif message.split(" ")[0] in ["/field", "field"]:
        services.change_settings_field(message.split('"')[1], message.split('"')[3])
        notification.answer(str(services.get_settings()).replace("'", '"'))
    elif message.split(" ")[0] in ["/ignore", "ignore"]:
        ignore_list = services.get_settings()["ignore"]
        number = services.normalize_number("".join(message.split(" ")[1:]))
        if number not in ignore_list:
            ignore_list.append(number)
            services.change_settings_field("ignore", ignore_list)
            notification.answer(str(services.get_settings()["ignore"]))
        else:
            notification.answer("Номер уже игнорируется")
    elif message.split(" ")[0] in ["/unignore", "unignore"]:
        ignore_list = services.get_settings()["ignore"]
        number = services.normalize_number("".join(message.split(" ")[1:]))
        ignore_list.remove(number)
        services.change_settings_field("ignore", ignore_list)
        notification.answer(str(services.get_settings()["ignore"]))
    elif message.split(" ")[0] in ["/redirect", "redirect"]:
        number = services.normalize_number("".join(message.split('"')[0].split(" ")[1:]))
        name = "".join(message.split('"')[1])
        redirects = services.get_settings()["redirect"]
        redirects[number] = name
        services.change_settings_field("redirect", redirects)
        notification.answer(str(services.get_settings()["redirect"]))
    elif message.split(" ")[0] in ["/unredirect", "unredirect"]:
        number = services.normalize_number("".join(message.split(" ")[1:]))
        redirects = services.get_settings()["redirect"]
        redirects.pop(number)
        services.change_settings_field("redirect", redirects)
        notification.answer(str(services.get_settings()["redirect"]))


if __name__ == "__main__":
    print("Starting bot...")
    bot.run_forever()
