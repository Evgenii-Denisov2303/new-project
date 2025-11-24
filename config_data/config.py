import os
from telebot import TeleBot
from dotenv import load_dotenv, find_dotenv
from pydantic.v1 import BaseSettings, SecretStr, StrictStr

# Проверка наличия обязательных переменных
if not find_dotenv():
    exit("Переменные окружения не загружены т.к. отсутствует файл .env")
else:
    load_dotenv()

class SiteSettings(BaseSettings):
    """
    Настройки сайта.

    Attributes:
        token (SecretStr): Токен бота.
        cat_api (StrictStr): Ключ API для котов.
        cat_facts_api (StrictStr): Ключ API для фактов о котах.
        translate_api (StrictStr): Ключ API для перевода.
    """
    token: SecretStr = os.getenv("BOT_TOKEN", None)
    cat_api: StrictStr = os.getenv("CAT_API_KEY", None)
    cat_facts_api: StrictStr = os.getenv("CAT_FACTS_API_KEY", None)
    translate_api: StrictStr = os.getenv("TRANSLATE_API_KEY", None)

# Определение команд по умолчанию
DEFAULT_COMMANDS = (
    ("start", "Запустить котика-ботика 2.0"),
    ("help", "Вывести справку"),
    ("survey", "Опрос")
)

"""
Команды по умолчанию для бота.

Attributes:
    DEFAULT_COMMANDS (tuple): Список кортежей с командами и их описаниями.
"""

# Пути к фотографиям
CAT_PHOTOS = {
    'Манечка': ["utils/cat_photos/Manechka.jpg",
                "utils/cat_photos/Manechka1.jpg",
                "utils/cat_photos/Manechka3.jpg",
                "utils/cat_photos/Manechka4.jpg"],
    'Цезарь': ["utils/cat_photos/Cezar.jpg",
               "utils/cat_photos/Cezar1.jpg",
               "utils/cat_photos/Cezar2.jpg"],
    'Шотландец': ["utils/cat_photos/shot.jpg",
                  "utils/cat_photos/shot1.jpg",
                  "utils/cat_photos/shot2.jpg"]
}

"""
Пути к фотографиям котов.

Attributes:
    CAT_PHOTOS (dict): Словарь с именами котов и списками путей к их фотографиям.
"""

# Инициализация настроек сайта
site = SiteSettings()

"""
Инициализация настроек сайта.

Attributes:
    site (SiteSettings): Экземпляр класса SiteSettings.
"""

# Проверка наличия токена бота
if not site.token:
    raise ValueError("Не указан токен бота в переменных окружения")

"""
Проверка наличия токена бота.

Raises:
    ValueError: Если токен бота не указан.
"""

# Инициализация бота
bot = TeleBot(site.token.get_secret_value())

"""
Инициализация бота Telegram.

Attributes:
    bot (TeleBot): Экземпляр класса TeleBot.
"""
