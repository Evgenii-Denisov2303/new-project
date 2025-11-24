from telebot import TeleBot
from typing import List
from config_data.config import CAT_PHOTOS
from services.cat_random_image_api import random_image_cat


def register_cat_photo_handlers(bot: TeleBot):
    """
    Регистрирует обработчики для фотографий котов.

    Args:
        bot (TeleBot): Экземпляр класса TeleBot.

    Returns:
        None
    """
    bot.register_message_handler(lambda message: show_manechka(message, bot),
                               func=lambda message: message.text == "Манечка😻")
    bot.register_message_handler(lambda message: show_cezar(message, bot),
                               func=lambda message: message.text == "Цезарь😸")
    bot.register_message_handler(lambda message: show_scottish(message, bot),
                               func=lambda message: message.text == "Шотландец😻")
    bot.register_message_handler(lambda message: show_random_cat(message, bot),
                               func=lambda message: message.text == "Рандомные котики😸")

def show_manechka(message, bot: TeleBot):
    """
    Отображает фотографии Манечки.

    Args:
        message (Message): Входящее сообщение.
        bot (TeleBot): Экземпляр класса TeleBot.

    Returns:
        None
    """
    bot.send_message(message.from_user.id, 'Увидеть Манечку можно здесь')
    send_photos(bot, message.chat.id, CAT_PHOTOS['Манечка'])

def show_cezar(message, bot: TeleBot):
    """
    Отображает фотографии Цезаря.

    Args:
        message (Message): Входящее сообщение.
        bot (TeleBot): Экземпляр класса TeleBot.

    Returns:
        None
    """
    bot.send_message(message.from_user.id, 'Увидеть Цезаря можно здесь')
    send_photos(bot, message.chat.id, CAT_PHOTOS['Цезарь'])

def show_scottish(message, bot: TeleBot):
    """
    Отображает фотографии Шотландца.

    Args:
        message (Message): Входящее сообщение.
        bot (TeleBot): Экземпляр класса TeleBot.

    Returns:
        None
    """
    bot.send_message(message.from_user.id, 'Увидеть Шотландца можно здесь')
    send_photos(bot, message.chat.id, CAT_PHOTOS['Шотландец'])

def show_random_cat(message, bot: TeleBot):
    """
    Отображает случайное фото кота.

    Args:
        message (Message): Входящее сообщение.
        bot (TeleBot): Экземпляр класса TeleBot.

    Returns:
        None
    """
    bot.send_photo(message.from_user.id, random_image_cat())
    bot.send_message(message.chat.id, text="Продолжай не останавливайся жмякать на рандомные фото котиков!")

def send_photos(bot: TeleBot, chat_id: int, photo_files: List[str]):
    """
    Отправляет несколько фотографий котов в чат.

    Args:
        bot (TeleBot): Экземпляр бота.
        chat_id (int): ID чата, куда отправлять фотографии.
        photo_files (List[str]): Список путей к файлам фотографий.

    Returns:
        None
    """
    for photo_path in photo_files:
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo)
        except FileNotFoundError:
            bot.send_message(chat_id, f"Извините, фото {photo_path} не найдено")
        except Exception as e:
            bot.send_message(chat_id, f"Произошла ошибка при отправке фото: {str(e)}")
