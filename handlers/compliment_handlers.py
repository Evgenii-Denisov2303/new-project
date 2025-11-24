from telebot import TeleBot
from utils.compliments_blanks import random_compliments


def register_compliment_handlers(bot: TeleBot):
    """
    Регистрирует обработчики для комплиментов.

    Args:
        bot (TeleBot): Экземпляр класса TeleBot.

    Returns:
        None
    """
    bot.register_message_handler(lambda message: show_compliment(message, bot),
                               func=lambda message: message.text == "Комплименты🥰")

def show_compliment(message, bot: TeleBot):
    """
    Отображает случайный комплимент и приглашение продолжать.

    Args:
        message (Message): Входящее сообщение.
        bot (TeleBot): Экземпляр класса TeleBot.

    Returns:
        None
    """
    bot.send_message(message.chat.id, text=f"{random_compliments()}")
    bot.send_message(message.chat.id, text="Продолжай не останавливайся жмякать на комплимент!")
