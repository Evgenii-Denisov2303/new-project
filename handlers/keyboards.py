from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📸 Фото", callback_data="menu:photos")
    builder.button(text="📚 Факты", callback_data="menu:facts")
    builder.button(text="✨ Настроение", callback_data="menu:fun")
    builder.button(text="🧼 Уход", callback_data="menu:useful")
    builder.button(text="⭐ Оценить", callback_data="survey:open")
    builder.button(text="ℹ️ Как пользоваться", callback_data="menu:help")
    builder.adjust(2, 2, 2)
    return builder.as_markup()


def photos_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Манечка", callback_data="photo:manechka")
    builder.button(text="Цезарь", callback_data="photo:cezar")
    builder.button(text="Шотландец", callback_data="photo:scottish")
    builder.button(text="🎲 Случайный", callback_data="photo:random")
    builder.button(text="⬅️ В меню", callback_data="menu:main")
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def fun_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔮 Гороскоп", callback_data="fun:horoscope")
    builder.button(text="💬 Комплимент", callback_data="fun:compliment")
    builder.button(text="🎮 Игра", callback_data="fun:game")
    builder.button(text="⬅️ В меню", callback_data="menu:main")
    builder.adjust(2, 1, 1)
    return builder.as_markup()


def useful_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="😽 Как гладить котиков", callback_data="useful:advice")
    builder.button(text="⬅️ В меню", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


def facts_nav_keyboard(has_prev: bool, has_next: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="⬅️",
        callback_data="facts:prev" if has_prev else "noop",
    )
    builder.button(text="🆕 Еще факт", callback_data="facts:new")
    builder.button(
        text="➡️",
        callback_data="facts:next" if has_next else "noop",
    )
    builder.button(text="⬅️ В меню", callback_data="menu:main")
    builder.adjust(3, 1)
    return builder.as_markup()


def survey_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⭐ Поставить оценку", callback_data="survey:rate")
    builder.button(text="💬 Оставить отзыв", callback_data="survey:comment")
    builder.button(text="⬅️ В меню", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


def zodiac_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    zodiac_signs = [
        ("Овен", "oven"),
        ("Телец", "telec"),
        ("Близнецы", "bliznecy"),
        ("Рак", "rak"),
        ("Лев", "lev"),
        ("Дева", "deva"),
        ("Весы", "vesy"),
        ("Скорпион", "scorpion"),
        ("Стрелец", "strelec"),
        ("Козерог", "kozerog"),
        ("Водолей", "vodoley"),
        ("Рыбы", "ryby"),
    ]
    for sign, callback in zodiac_signs:
        builder.button(text=sign, callback_data=f"zodiac:{callback}")
    builder.button(text="⬅️ В меню", callback_data="menu:main")
    builder.adjust(3, 3, 3, 3, 1)
    return builder.as_markup()


def action_menu_keyboard(action_text: str, action_data: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=action_text, callback_data=action_data)
    builder.button(text="⬅️ В меню", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ В меню", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()
