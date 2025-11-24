from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS

def set_default_commands(bot):
    """
    Устанавливает команды по умолчанию для бота.

    Args:
        bot (TeleBot): Экземпляр класса TeleBot.

    Returns:
        None
    """
    bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS])

