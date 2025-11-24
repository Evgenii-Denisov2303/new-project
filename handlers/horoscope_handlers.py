from telebot import TeleBot, types
from utils.compliments_blanks import generate_horoscope


def get_zodiac_keyboard():
    """
    Создает клавиатуру для выбора знака зодиака.

    Returns:
        types.InlineKeyboardMarkup: Клавиатура с кнопками знаков зодиака.
    """
    keyboard = types.InlineKeyboardMarkup()
    zodiac_signs = {
        "Овен": "oven", "Телец": "telec", "Близнецы": "bliznecy", "Рак": "rak",
        "Лев": "lev", "Дева": "deva", "Весы": "vesy", "Скорпион": "scorpion",
        "Стрелец": "strelec", "Козерог": "kozerog", "Водолей": "vodoley", "Рыбы": "ryby"
    }
    for sign, callback in zodiac_signs.items():
        keyboard.add(types.InlineKeyboardButton(text=sign, callback_data=callback))
    return keyboard

def register_horoscope_handlers(bot: TeleBot):
    """
    Регистрирует обработчики для гороскопа.

    Args:
        bot (TeleBot): Экземпляр класса TeleBot.

    Returns:
        None
    """
    bot.register_message_handler(lambda message: show_horoscope(message, bot),
                               func=lambda message: message.text == "Гороскоп🥰")
    bot.register_callback_query_handler(lambda message: callback_inline(message, bot),
                                      func=lambda call: call.data in [
                                          "oven", "telec", "bliznecy", "rak", "lev", "deva",
                                          "vesy", "scorpion", "strelec", "kozerog", "vodoley", "ryby"
                                      ])

def show_horoscope(message, bot: TeleBot):
    """
    Отображает сообщение о выборе гороскопа и предлагает выбрать знак зодиака.

    Args:
        message (Message): Входящее сообщение.
        bot (TeleBot): Экземпляр класса TeleBot.

    Returns:
        None
    """
    bot.send_message(message.chat.id, text="Сейчас я расскажу тебе гороскоп на сегодня.")
    keyboard = get_zodiac_keyboard()
    bot.send_message(message.chat.id,
                   text="Выбери свой знак зодиака, {0.first_name}".format(message.from_user),
                   reply_markup=keyboard)

def callback_inline(call, bot: TeleBot):
    """
    Обработчик нажатия на кнопку знака зодиака.

    Args:
        call (CallbackQuery): Callback запрос.
        bot (TeleBot): Экземпляр класса TeleBot.

    Returns:
        None
    """
    bot.send_message(call.message.chat.id, generate_horoscope())
