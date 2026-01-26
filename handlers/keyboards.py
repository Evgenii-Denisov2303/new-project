from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.i18n import t, LANGUAGE_NAMES


def photos_menu_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Манечка", callback_data="photo:manechka")
    builder.button(text="Цезарь", callback_data="photo:cezar")
    builder.button(text="Шотландец", callback_data="photo:scottish")
    builder.button(text=t(lang, "btn.random"), callback_data="photo:random")
    builder.adjust(2, 2)
    return builder.as_markup()


def fun_menu_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(lang, "btn.horoscope"), callback_data="fun:horoscope")
    builder.button(text=t(lang, "btn.compliment"), callback_data="fun:compliment")
    builder.button(text=t(lang, "btn.game"), callback_data="fun:game")
    builder.adjust(2, 1)
    return builder.as_markup()


def useful_menu_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(lang, "btn.useful_advice"), callback_data="useful:advice")
    builder.adjust(1)
    return builder.as_markup()


def facts_nav_keyboard(has_prev: bool, has_next: bool, lang: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="⬅️",
        callback_data="facts:prev" if has_prev else "noop",
    )
    builder.button(text=t(lang, "btn.new_fact"), callback_data="facts:new")
    builder.button(
        text="➡️",
        callback_data="facts:next" if has_next else "noop",
    )
    builder.adjust(3)
    return builder.as_markup()


def survey_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(lang, "btn.rate_poll"), callback_data="survey:rate")
    builder.button(text=t(lang, "btn.comment"), callback_data="survey:comment")
    builder.adjust(1)
    return builder.as_markup()


def zodiac_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    zodiac_signs = {
        "ru": [
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
        ],
        "en": [
            ("Aries", "oven"),
            ("Taurus", "telec"),
            ("Gemini", "bliznecy"),
            ("Cancer", "rak"),
            ("Leo", "lev"),
            ("Virgo", "deva"),
            ("Libra", "vesy"),
            ("Scorpio", "scorpion"),
            ("Sagittarius", "strelec"),
            ("Capricorn", "kozerog"),
            ("Aquarius", "vodoley"),
            ("Pisces", "ryby"),
        ],
        "cs": [
            ("Beran", "oven"),
            ("Býk", "telec"),
            ("Blíženci", "bliznecy"),
            ("Rak", "rak"),
            ("Lev", "lev"),
            ("Panna", "deva"),
            ("Váhy", "vesy"),
            ("Štír", "scorpion"),
            ("Střelec", "strelec"),
            ("Kozoroh", "kozerog"),
            ("Vodnář", "vodoley"),
            ("Ryby", "ryby"),
        ],
    }
    signs = zodiac_signs.get(lang, zodiac_signs["ru"])
    for sign, callback in signs:
        builder.button(text=sign, callback_data=f"zodiac:{callback}")
    builder.adjust(3, 3, 3, 3)
    return builder.as_markup()


def action_menu_keyboard(
    action_text: str,
    action_data: str,
    include_menu: bool = True,
    lang: str = "ru",
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=action_text, callback_data=action_data)
    if include_menu:
        builder.button(text=t(lang, "btn.menu"), callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


def bottom_menu_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t(lang, "btn.photos")),
                KeyboardButton(text=t(lang, "btn.fun")),
                KeyboardButton(text=t(lang, "btn.facts")),
            ],
            [
                KeyboardButton(text=t(lang, "btn.useful")),
                KeyboardButton(text=t(lang, "btn.help")),
                KeyboardButton(text=t(lang, "btn.rate")),
            ],
            [KeyboardButton(text=t(lang, "btn.language"))],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder=t(lang, "menu.placeholder"),
        selective=False,
        is_persistent=True,  # <- важно: просим Telegram держать клавиатуру
    )


def language_keyboard(current_lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for lang_code, label in LANGUAGE_NAMES.items():
        text = f"✅ {label}" if lang_code == current_lang else label
        builder.button(text=text, callback_data=f"lang:set:{lang_code}")
    builder.adjust(2, 1)
    return builder.as_markup()
