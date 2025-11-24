from telebot import TeleBot, types
from config_data.config import bot

# Константы для текстов кнопок
GREETING_BUTTON = "👋 Поздороваться"
BUTTON_TEXTS = {
    "cats": ["Манечка😻", "Цезарь😸", "Шотландец😻"],
    "features": ["Как гладить котиков😽", "Игра про котиков😽"],
    "fun": ["Гороскоп🥰", "Комплименты🥰"],
    "content": ["Факты о котиках😻", "Рандомные котики😸"]
}

"""
Константы для текстов кнопок в интерфейсе бота:
- cats: Кнопки с именами котиков
- features: Функциональные возможности
- fun: Развлекательные функции
- content: Контентные разделы
"""

HELP_TEXT = (
    "🐱 *Котик-бот* - ваш помощник для поднятия настроения! 🐱\n\n"
    "*Доступные команды:*\n"
    "/start - Запустить бота\n"
    "/help - Показать эту справку\n"
    "/survey - Оценить бота\n\n"
    "*Доступные функции:*\n"
    "• Фотографии котиков (Манечка, Цезарь, Шотландец)\n"
    "• Факты о котиках\n"
    "• Рандомные фото котиков\n"
    "• Гороскоп\n"
    "• Комплименты\n"
    "• Советы по уходу за котиками\n"
    "• Игры про котиков\n\n"
    "Просто нажмите на кнопку '👋 Поздороваться', чтобы начать!"
)

"""
Текст справки для бота. Содержит список команд и доступных функций.
"""

# ================= Клавиатуры =================

def get_start_keyboard() -> types.ReplyKeyboardMarkup:
    """
    Создает стартовую клавиатуру с кнопкой приветствия.

    Returns:
        types.ReplyKeyboardMarkup: Клавиатура с единственной кнопкой GREETING_BUTTON
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(GREETING_BUTTON))
    return markup

def get_main_keyboard() -> types.ReplyKeyboardMarkup:
    """
    Генерирует основную клавиатуру с функциями бота.

    Кнопки группируются по категориям:
    - Котики
    - Функции
    - Развлечения
    - Контент

    Returns:
        types.ReplyKeyboardMarkup: Основная клавиатура с кнопками функций
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    cat_buttons = [types.KeyboardButton(text) for text in BUTTON_TEXTS["cats"]]
    feature_buttons = [types.KeyboardButton(text) for text in BUTTON_TEXTS["features"]]
    fun_buttons = [types.KeyboardButton(text) for text in BUTTON_TEXTS["fun"]]
    content_buttons = [types.KeyboardButton(text) for text in BUTTON_TEXTS["content"]]

    markup.add(*cat_buttons, *feature_buttons, *fun_buttons, *content_buttons)

    return markup

def get_survey_keyboard() -> types.InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для опроса пользователей.

    Returns:
        types.InlineKeyboardMarkup: Клавиатура с двумя кнопками:
        - Поставить рейтинг
        - Оставить комментарий
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("⭐ Поставить рейтинг", callback_data="rate_bot"),
        types.InlineKeyboardButton("💬 Оставить комментарий", callback_data="leave_comment")
    )
    return markup

# ================= Обработчики команд =================

def start_command(message: types.Message, bot: TeleBot) -> None:
    """
    Обрабатывает команду /start. Инициализирует взаимодействие с пользователем.

    Args:
        message (types.Message): Входящее сообщение от пользователя
        bot (TeleBot): Экземпляр телеграм-бота
    """
    markup = get_start_keyboard()
    bot.send_message(
        message.chat.id,
        f"👋 Привет, {message.from_user.first_name}! Я твой бот-помошник для просмотра умилительных котят. Нажми поздороваться!",
        reply_markup=markup
    )

def help_command(message: types.Message, bot: TeleBot) -> None:
    """
    Обрабатывает команду /help. Отправляет пользователю справочную информацию.

    Args:
        message (types.Message): Входящее сообщение от пользователя
        bot (TeleBot): Экземпляр телеграм-бота
    """
    bot.send_message(message.chat.id, HELP_TEXT, parse_mode='Markdown')

def survey_command(message: types.Message, bot: TeleBot) -> None:
    """
    Обрабатывает команду /survey. Отправляет клавиатуру для оценки работы бота.

    Args:
        message (types.Message): Входящее сообщение от пользователя
        bot (TeleBot): Экземпляр телеграм-бота
    """
    markup = get_survey_keyboard()
    bot.send_message(
        message.chat.id,
        "📊 *Оцените нашего бота!*\n\nВы можете:\n1. Поставить рейтинг.\n2. Оставить комментарий.",
        parse_mode='Markdown',
        reply_markup=markup
    )

# ================= Обработчики кнопок =================

def greet_handler(message: types.Message, bot: TeleBot) -> None:
    """
    Обрабатывает нажатие кнопки приветствия. Показывает основное меню.

    Args:
        message (types.Message): Входящее сообщение от пользователя
        bot (TeleBot): Экземпляр телеграм-бота
    """
    markup = get_main_keyboard()
    bot.send_message(
        message.chat.id,
        "Я могу поддержать тебя и поднять настроение. ❓ Выбери интересующий тебя раздел.",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "rate_bot")
def rate_bot_handler(call: types.CallbackQuery) -> None:
    """
    Обрабатывает нажатие кнопки рейтинга. Создает опрос для оценки бота.

    Args:
        call (types.CallbackQuery): Входящий callback от inline-кнопки
    """
    bot.send_poll(
        chat_id=call.message.chat.id,
        question="⭐ Как вы оцениваете нашего бота?",
        options=["1️⃣ Плохо", "2️⃣", "3️⃣", "4️⃣", "5️⃣ Отлично"],
        is_anonymous=False,
        allows_multiple_answers=False
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "leave_comment")
def leave_comment_handler(call: types.CallbackQuery) -> None:
    """
    Инициирует процесс получения комментария от пользователя.

    Args:
        call (types.CallbackQuery): Входящий callback от inline-кнопки
    """
    msg = bot.send_message(
        call.message.chat.id,
        "💬 Напишите ваш комментарий о работе бота:",
        reply_markup=types.ForceReply(selective=True)
    )
    bot.register_next_step_handler(msg, handle_comment)
    bot.answer_callback_query(call.id)

# ================= Обработчики сообщений =================

@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.text.startswith(
    "💬 Напишите ваш комментарий"))
def handle_comment(message):
    """
    Обработчик текста комментария. Сохраняет в UTF-8.
    """
    user_comment = message.text
    user_id = message.from_user.id

    with open("comments.txt", "a", encoding="utf-8") as file:
        file.write(f"User {user_id}: {user_comment}\n")

    bot.send_message(message.chat.id, "Спасибо за ваш отзыв! 😊")


def unknown_command(message: types.Message, bot: TeleBot) -> None:
    """
    Обрабатывает неизвестные команды. Перенаправляет пользователя к основному меню.

    Args:
        message (types.Message): Входящее сообщение от пользователя
        bot (TeleBot): Экземпляр телеграм-бота
    """
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name} 👋\nВоспользуйтесь кнопками"
    )

# ================= Регистрация обработчиков =================

def register_basic_handlers(bot: TeleBot) -> None:
    """
    Регистрирует все базовые обработчики команд и сообщений.

    Args:
        bot (TeleBot): Экземпляр телеграм-бота для регистрации обработчиков
    """
    bot.register_message_handler(
        lambda message: start_command(message, bot),
        commands=['start']
    )
    bot.register_message_handler(
        lambda message: help_command(message, bot),
        commands=['help']
    )
    bot.register_message_handler(
        lambda message: survey_command(message, bot),
        commands=['survey']
    )
    bot.register_message_handler(
        lambda message: greet_handler(message, bot),
        func=lambda message: message.text == GREETING_BUTTON
    )
    bot.register_message_handler(
        lambda message: unknown_command(message, bot),
        func=lambda message: True
    )
