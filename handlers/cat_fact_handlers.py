import json
from telebot import TeleBot, types
from typing import List, Dict, Any, Optional, Tuple
from database.common.models import CatFact
from services.cat_fact_api import get_cat_fact
from services.translate_api import translate_text


def register_cat_fact_handlers(bot: TeleBot) -> None:
    """Регистрирует обработчики для фактов о котах."""
    bot.register_message_handler(
        lambda message: show_cat_fact(message, bot),
        func=lambda message: message.text == "Факты о котиках😻",
    )

    bot.register_callback_query_handler(
        lambda call: handle_fact_navigation(call, bot),
        func=lambda call: call.data.startswith("fact_"),
    )


def show_cat_fact(message: types.Message, bot: TeleBot) -> None:
    """Обработчик для кнопки 'Факты о котиках'."""
    message_text, markup = send_cat_fact(
        message.chat.id, message.from_user.id, is_new=True
    )
    bot.send_message(message.chat.id, message_text, reply_markup=markup)


def handle_fact_navigation(call: types.CallbackQuery, bot: TeleBot) -> None:
    """Обработчик навигации по фактам о котах."""
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    action = call.data.split("_")[1]  # fact_{action}

    user_fact = CatFact.get_or_create(user_id=user_id)
    facts = parse_facts(user_fact.facts)

    # Обработка новых фактов
    if action == "new":
        fact_text, markup = send_cat_fact(chat_id, user_id, is_new=True)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=fact_text,
            reply_markup=markup,
        )
        bot.answer_callback_query(call.id)
        return

    # Навигация по сохраненным фактам
    current_index = user_fact.current_index

    if action == "prev" and current_index > 0:
        user_fact.current_index -= 1
    elif action == "next" and current_index < len(facts) - 1:
        user_fact.current_index += 1

    user_fact.save()

    # Обновление сообщения с новым фактом
    fact_text, markup = send_cat_fact(chat_id, user_id, is_new=False)
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=fact_text,
        reply_markup=markup,
    )
    bot.answer_callback_query(call.id)


def send_cat_fact(chat_id, user_id, is_new=False) -> Tuple[str, types.InlineKeyboardMarkup]:
    """Генерирует текст факта и клавиатуру навигации."""
    user_fact = CatFact.get_or_create(user_id=user_id)

    # Получение нового факта
    if is_new:
        fact_text = get_cat_fact()
        if not fact_text:
            return "Не удалось получить факт о котах. Попробуйте позже.", create_nav_markup(user_fact)

        translated_text = translate_text(fact_text)
        display_text = format_display_text(fact_text, translated_text)

        facts = json.loads(user_fact.facts) if user_fact.facts else []
        facts.append({
            "text": fact_text,
            "translation": translated_text,
            "display_text": display_text
        })

        user_fact.facts = json.dumps(facts)
        user_fact.current_index = len(facts) - 1
        user_fact.save()
    else:
        # Получение сохраненного факта
        facts = json.loads(user_fact.facts) if user_fact.facts else []
        if not facts:
            return "У вас пока нет сохраненных фактов о котах.", create_nav_markup(user_fact)

        fact_data = facts[user_fact.current_index]
        display_text = fact_data.get("display_text", format_display_text(
            fact_data.get("text", ""),
            fact_data.get("translation", "")
        ))

    return display_text, create_nav_markup(user_fact)


def create_nav_markup(user_fact: CatFact) -> types.InlineKeyboardMarkup:
    """Создает клавиатуру навигации с учетом текущей позиции."""
    markup = types.InlineKeyboardMarkup(row_width=3)
    facts = json.loads(user_fact.facts) if user_fact.facts else []
    current_index = user_fact.current_index

    buttons = [
        types.InlineKeyboardButton("⬅️ Пред", callback_data="fact_prev"),
        types.InlineKeyboardButton("🆕 Новый", callback_data="fact_new"),
        types.InlineKeyboardButton("След ➡️", callback_data="fact_next")
    ]

    # Автоматическая активация/деактивация кнопок
    if current_index <= 0:
        buttons[0] = types.InlineKeyboardButton("⬅️", callback_data="none")
    if current_index >= len(facts) - 1:
        buttons[2] = types.InlineKeyboardButton("➡️", callback_data="none")

    markup.add(*buttons)
    return markup


def format_display_text(original: str, translation: str) -> str:
    """Форматирует текст для отображения."""
    return f"🇬🇧 {original}\n\n🇷🇺 {translation}" if translation else f"🇬🇧 {original}\n\n❌ Перевод недоступен"


def parse_facts(facts_json: Optional[str]) -> List[Dict[str, Any]]:
    """Безопасно разбирает JSON с фактами."""
    if not facts_json:
        return []

    try:
        return json.loads(facts_json)
    except json.JSONDecodeError:
        return []
