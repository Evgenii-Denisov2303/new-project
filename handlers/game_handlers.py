from telebot import TeleBot


def register_game_handlers(bot: TeleBot):
    """
    Регистрирует обработчики для игры про котиков.

    Args:
        bot (TeleBot): Экземпляр класса TeleBot.

    Returns:
        None
    """
    bot.register_message_handler(lambda message: show_game(message, bot),
                               func=lambda message: message.text == "Игра про котиков😽")

def show_game(message, bot: TeleBot):
    """
    Отображает ссылку на игру про котиков.

    Args:
        message (Message): Входящее сообщение.
        bot (TeleBot): Экземпляр класса TeleBot.

    Returns:
        None
    """
    bot.send_message(message.from_user.id, 'https://t.me/catizenbot/gameapp?startapp=r_3_2007855',
                   parse_mode='Markdown')
