from __future__ import annotations

from database.db_setup import get_user_language, set_user_language
from utils.cache import TTLCache


SUPPORTED_LANGS = ("ru", "en", "cs")
DEFAULT_LANG = "ru"

_LANG_CACHE = TTLCache(max_items=4096)
_LANG_CACHE_TTL = 60 * 60 * 6  # 6 hours

LANGUAGE_NAMES = {
    "ru": "Русский",
    "en": "English",
    "cs": "Čeština",
}

TRANSLATIONS = {
    "ru": {
        "menu.welcome": "🐾🐾 <b>Котик-ботик</b>\nВыбери раздел кнопками снизу 👇\n────────",
        "menu.help": "ℹ️ <b>Помощь</b>\n• Нажимай кнопки снизу (Фото/Настроение/Факты/Уход)\n• Внутри разделов используй кнопки под сообщениями\n• Если клавиатура пропала — напиши /menu\n────────",
        "menu.photos": "📸 <b>Фото котиков</b>\nВыбери котика или нажми 🎲 случайный.\n────────",
        "menu.fun": "✨ <b>Настроение</b>\nГороскоп, комплимент или мини-игра.\n────────",
        "menu.useful": "😽 <b>Уход</b>\nСоветы по котикам.\n────────",
        "menu.survey": "⭐ <b>Оценить бота</b>\nВыбери действие.\n────────",
        "menu.fallback": "Нажми кнопки снизу 👇 или напиши /menu",
        "menu.choose_below": "Выбери раздел ниже 👇",
        "menu.placeholder": "Выбери раздел кнопками ниже 👇",
        "lang.choose": "🌍 <b>Язык</b>\nВыбери язык:\n────────",
        "lang.updated": "Язык обновлён ✅",
        "facts.hub": "📚 <b>Факты</b>\nНажимай «Новый», чтобы получать факты.\n────────",
        "facts.title": "🧠 <b>Кошачий факт</b>\n────────",
        "facts.no_translation": "❌ Перевод недоступен",
        "facts.fetch_error": "Не удалось получить факт.",
        "facts.busy": "Я чуть занят 😺 Попробуй снова.",
        "facts.none": "Фактов пока нет. Нажми «Новый».",
        "photos.hub": "📸 <b>Фото котиков</b>\nВыбери любимчика или нажми случайный кадр.\n────────",
        "photos.random_caption": "🎲 <b>Случайный котик</b>\n────────\nВот тебе котик 🐾",
        "photos.random_error": "🎲 <b>Случайный котик</b>\n────────\nНе удалось получить фото. Попробуй чуть позже.",
        "photos.album_done": "📸 <b>{title}</b>\n────────\nГотово. Хочешь еще?",
        "fun.hub": "✨ <b>Настроение</b>\nХочешь комплимент, гороскоп или игру?\n────────",
        "fun.compliment_title": "💖 <b>Комплимент</b>\n────────\n{value}",
        "fun.game_title": "🎮 <b>Кошачья игра</b>\n────────\nЗапускай: {url}",
        "fun.horoscope_choose": "🔮 <b>Гороскоп</b>\nВыбери знак зодиака:\n────────",
        "fun.horoscope_result": "🔮 <b>Твой гороскоп</b>\n────────\n{value}",
        "useful.text": "😽 <b>Как гладить котика</b>\n────────\nКороткая статья и советы:\nhttps://www.feliway.com/ru/Nash-blog/Kak-pravil-no-gladit-koshku/",
        "survey.title": "⭐ <b>Оценка</b>\n────────\nОцени бота или оставь отзыв.",
        "survey.poll_question": "Как тебе котик-ботик?",
        "survey.thanks": "Спасибо! Хочешь еще что-то посмотреть?\n────────",
        "survey.ask_comment": "💬 Напиши отзыв одним сообщением.\n────────",
        "survey.empty_comment": "Похоже, отзыв пустой. Попробуй еще раз.",
        "survey.thanks_comment": "Спасибо за отзыв! 🐾",
        "btn.photos": "Фото",
        "btn.fun": "Настроение",
        "btn.facts": "Факты",
        "btn.useful": "Уход",
        "btn.help": "Помощь",
        "btn.rate": "Оценить",
        "btn.language": "Язык",
        "btn.menu": "⬅️ В меню",
        "btn.horoscope": "🔮 Гороскоп",
        "btn.compliment": "💬 Комплимент",
        "btn.game": "🎮 Игра",
        "btn.useful_advice": "😽 Как гладить котиков",
        "btn.more_photo": "Еще фото",
        "btn.more_random": "🎲 Случайный котик",
        "btn.more_fun": "Еще настроение",
        "btn.more_compliment": "Еще комплимент",
        "btn.more_horoscope": "Еще гороскоп",
        "btn.more_useful": "Еще полезное",
        "btn.rate_poll": "⭐ Поставить оценку",
        "btn.comment": "💬 Оставить отзыв",
        "btn.new_fact": "🆕 Еще факт",
        "btn.random": "🎲 Случайный",
    },
    "en": {
        "menu.welcome": "🐾🐾 <b>Cat Bot</b>\nChoose a section below 👇\n────────",
        "menu.help": "ℹ️ <b>Help</b>\n• Use the buttons below (Photos/Mood/Facts/Care)\n• Use inline buttons inside sections\n• If the keyboard is gone — type /menu\n────────",
        "menu.photos": "📸 <b>Cat photos</b>\nPick a cat or tap 🎲 random.\n────────",
        "menu.fun": "✨ <b>Mood</b>\nHoroscope, compliment, or mini‑game.\n────────",
        "menu.useful": "😽 <b>Care</b>\nTips for cat lovers.\n────────",
        "menu.survey": "⭐ <b>Rate the bot</b>\nChoose an action.\n────────",
        "menu.fallback": "Use the buttons below 👇 or type /menu",
        "menu.choose_below": "Choose a section below 👇",
        "menu.placeholder": "Choose a section below 👇",
        "lang.choose": "🌍 <b>Language</b>\nChoose language:\n────────",
        "lang.updated": "Language updated ✅",
        "facts.hub": "📚 <b>Facts</b>\nTap “New” to get facts.\n────────",
        "facts.title": "🧠 <b>Cat fact</b>\n────────",
        "facts.no_translation": "❌ Translation unavailable",
        "facts.fetch_error": "Failed to fetch a fact.",
        "facts.busy": "I’m a bit busy 😺 Try again.",
        "facts.none": "No facts yet. Tap “New”.",
        "photos.hub": "📸 <b>Cat photos</b>\nPick a favorite or tap a random shot.\n────────",
        "photos.random_caption": "🎲 <b>Random cat</b>\n────────\nHere’s a cat 🐾",
        "photos.random_error": "🎲 <b>Random cat</b>\n────────\nCouldn’t fetch a photo. Try later.",
        "photos.album_done": "📸 <b>{title}</b>\n────────\nDone. Want more?",
        "fun.hub": "✨ <b>Mood</b>\nWant a compliment, horoscope, or game?\n────────",
        "fun.compliment_title": "💖 <b>Compliment</b>\n────────\n{value}",
        "fun.game_title": "🎮 <b>Cat game</b>\n────────\nLaunch: {url}",
        "fun.horoscope_choose": "🔮 <b>Horoscope</b>\nChoose your zodiac sign:\n────────",
        "fun.horoscope_result": "🔮 <b>Your horoscope</b>\n────────\n{value}",
        "useful.text": "😽 <b>How to pet a cat</b>\n────────\nShort article and tips:\nhttps://www.feliway.com/ru/Nash-blog/Kak-pravil-no-gladit-koshku/",
        "survey.title": "⭐ <b>Rating</b>\n────────\nRate the bot or leave feedback.",
        "survey.poll_question": "How do you like the cat bot?",
        "survey.thanks": "Thanks! Want to see more?\n────────",
        "survey.ask_comment": "💬 Write your feedback in one message.\n────────",
        "survey.empty_comment": "Looks like an empty message. Try again.",
        "survey.thanks_comment": "Thanks for the feedback! 🐾",
        "btn.photos": "Photos",
        "btn.fun": "Mood",
        "btn.facts": "Facts",
        "btn.useful": "Care",
        "btn.help": "Help",
        "btn.rate": "Rate",
        "btn.language": "Language",
        "btn.menu": "⬅️ Back to menu",
        "btn.horoscope": "🔮 Horoscope",
        "btn.compliment": "💬 Compliment",
        "btn.game": "🎮 Game",
        "btn.useful_advice": "😽 How to pet cats",
        "btn.more_photo": "More photos",
        "btn.more_random": "🎲 Random cat",
        "btn.more_fun": "More mood",
        "btn.more_compliment": "Another compliment",
        "btn.more_horoscope": "Another horoscope",
        "btn.more_useful": "More tips",
        "btn.rate_poll": "⭐ Rate",
        "btn.comment": "💬 Leave feedback",
        "btn.new_fact": "🆕 New fact",
        "btn.random": "🎲 Random",
    },
    "cs": {
        "menu.welcome": "🐾🐾 <b>Kočičí bot</b>\nVyber sekci níže 👇\n────────",
        "menu.help": "ℹ️ <b>Nápověda</b>\n• Používej tlačítka dole (Fotky/Nálada/Fakta/Péče)\n• Uvnitř sekcí použij tlačítka pod zprávami\n• Pokud klávesnice zmizí — napiš /menu\n────────",
        "menu.photos": "📸 <b>Kočičí fotky</b>\nVyber kočku nebo klepni 🎲 náhodně.\n────────",
        "menu.fun": "✨ <b>Nálada</b>\nHoroskop, kompliment nebo hra.\n────────",
        "menu.useful": "😽 <b>Péče</b>\nTipy pro milovníky koček.\n────────",
        "menu.survey": "⭐ <b>Ohodnotit bota</b>\nVyber akci.\n────────",
        "menu.fallback": "Použij tlačítka dole 👇 nebo napiš /menu",
        "menu.choose_below": "Vyber sekci níže 👇",
        "menu.placeholder": "Vyber sekci níže 👇",
        "lang.choose": "🌍 <b>Jazyk</b>\nVyber jazyk:\n────────",
        "lang.updated": "Jazyk aktualizován ✅",
        "facts.hub": "📚 <b>Fakta</b>\nKlepni „Nové“ pro další fakta.\n────────",
        "facts.title": "🧠 <b>Kočičí fakt</b>\n────────",
        "facts.no_translation": "❌ Překlad není dostupný",
        "facts.fetch_error": "Nepodařilo se získat fakt.",
        "facts.busy": "Jsem zaneprázdněný 😺 Zkus to znovu.",
        "facts.none": "Zatím žádná fakta. Klepni „Nové“.",
        "photos.hub": "📸 <b>Kočičí fotky</b>\nVyber favorita nebo náhodný snímek.\n────────",
        "photos.random_caption": "🎲 <b>Náhodná kočka</b>\n────────\nTady máš kočku 🐾",
        "photos.random_error": "🎲 <b>Náhodná kočka</b>\n────────\nFoto se nepodařilo získat. Zkus později.",
        "photos.album_done": "📸 <b>{title}</b>\n────────\nHotovo. Chceš další?",
        "fun.hub": "✨ <b>Nálada</b>\nChceš kompliment, horoskop nebo hru?\n────────",
        "fun.compliment_title": "💖 <b>Kompliment</b>\n────────\n{value}",
        "fun.game_title": "🎮 <b>Kočičí hra</b>\n────────\nSpusť: {url}",
        "fun.horoscope_choose": "🔮 <b>Horoskop</b>\nVyber znamení zvěrokruhu:\n────────",
        "fun.horoscope_result": "🔮 <b>Tvůj horoskop</b>\n────────\n{value}",
        "useful.text": "😽 <b>Jak hladit kočku</b>\n────────\nKrátký článek a tipy:\nhttps://www.feliway.com/ru/Nash-blog/Kak-pravil-no-gladit-koshku/",
        "survey.title": "⭐ <b>Hodnocení</b>\n────────\nOhodnoť bota nebo zanech recenzi.",
        "survey.poll_question": "Jak se ti líbí kočičí bot?",
        "survey.thanks": "Díky! Chceš vidět víc?\n────────",
        "survey.ask_comment": "💬 Napiš recenzi jednou zprávou.\n────────",
        "survey.empty_comment": "Zpráva je prázdná. Zkus to znovu.",
        "survey.thanks_comment": "Díky za recenzi! 🐾",
        "btn.photos": "Fotky",
        "btn.fun": "Nálada",
        "btn.facts": "Fakta",
        "btn.useful": "Péče",
        "btn.help": "Nápověda",
        "btn.rate": "Hodnotit",
        "btn.language": "Jazyk",
        "btn.menu": "⬅️ Zpět do menu",
        "btn.horoscope": "🔮 Horoskop",
        "btn.compliment": "💬 Kompliment",
        "btn.game": "🎮 Hra",
        "btn.useful_advice": "😽 Jak hladit kočky",
        "btn.more_photo": "Další fotky",
        "btn.more_random": "🎲 Náhodná kočka",
        "btn.more_fun": "Další nálada",
        "btn.more_compliment": "Další kompliment",
        "btn.more_horoscope": "Další horoskop",
        "btn.more_useful": "Další tipy",
        "btn.rate_poll": "⭐ Ohodnotit",
        "btn.comment": "💬 Zanechat recenzi",
        "btn.new_fact": "🆕 Nový fakt",
        "btn.random": "🎲 Náhodný",
    },
}


def t(lang: str, key: str) -> str:
    bundle = TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANG])
    return bundle.get(key, TRANSLATIONS[DEFAULT_LANG].get(key, key))


def text_variants(key: str) -> list[str]:
    values = []
    for lang in SUPPORTED_LANGS:
        value = TRANSLATIONS.get(lang, {}).get(key)
        if value:
            values.append(value)
    return values


def normalize_lang(code: str | None) -> str:
    if not code:
        return DEFAULT_LANG
    code = code.lower()
    if code.startswith("ru"):
        return "ru"
    if code.startswith("en"):
        return "en"
    if code.startswith("cs") or code.startswith("cz"):
        return "cs"
    return DEFAULT_LANG


async def resolve_user_lang(user_id: int, telegram_code: str | None) -> str:
    cached = _LANG_CACHE.get(user_id)
    if cached in SUPPORTED_LANGS:
        return cached

    lang = await get_user_language(user_id)
    if lang in SUPPORTED_LANGS:
        _LANG_CACHE.set(user_id, lang, ttl=_LANG_CACHE_TTL)
        return lang
    lang = normalize_lang(telegram_code)
    await set_user_language(user_id, lang)
    _LANG_CACHE.set(user_id, lang, ttl=_LANG_CACHE_TTL)
    return lang


async def set_user_language_cached(user_id: int, language: str) -> None:
    await set_user_language(user_id, language)
    _LANG_CACHE.set(user_id, language, ttl=_LANG_CACHE_TTL)
