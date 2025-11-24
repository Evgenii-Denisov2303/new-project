from telebot import TeleBot


def register_advice_handlers(bot: TeleBot):
    """
    Регистрирует обработчики для совета по уходу за котами.

    Args:
        bot (TeleBot): Экземпляр класса TeleBot.

    Returns:
        None
    """
    bot.register_message_handler(lambda message: show_advice(message, bot),
                                 func=lambda message: message.text == "Как гладить котиков😽")

def show_advice(message, bot: TeleBot):
    """
    Отображает советы по уходу за котами.

    Args:
        message (Message): Входящее сообщение.
        bot (TeleBot): Экземпляр класса TeleBot.

    Returns:
        None
    """
    bot.send_message(message.from_user.id,
                   "Советы как гладить кошечек можете прочитать в публикации по "
                   "[ссылке](https://www.feliway.com/ru/Nash-blog/Kak-pravil-no-gladit-koshku/)"
                   , parse_mode='Markdown')
