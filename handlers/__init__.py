from telebot import TeleBot
from .cat_photo_handlers import register_cat_photo_handlers
from .compliment_handlers import register_compliment_handlers
from .horoscope_handlers import register_horoscope_handlers
from .advice_handlers import register_advice_handlers
from .game_handlers import register_game_handlers
from .cat_fact_handlers import register_cat_fact_handlers
from .basic_handlers import register_basic_handlers

def register_all_handlers(bot: TeleBot):
    """
    Регистрирует все обработчики для бота.

    Args:
        bot (TeleBot): Экземпляр класса TeleBot.

    Returns:
        None
    """
    # Регистрация всех обработчиков
    register_cat_photo_handlers(bot)
    register_compliment_handlers(bot)
    register_horoscope_handlers(bot)
    register_advice_handlers(bot)
    register_game_handlers(bot)
    register_cat_fact_handlers(bot)
    register_basic_handlers(bot)
