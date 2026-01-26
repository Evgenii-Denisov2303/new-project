from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from handlers.keyboards import (
    bottom_menu_keyboard,
    photos_menu_keyboard,
    fun_menu_keyboard,
    useful_menu_keyboard,
    survey_keyboard,
    language_keyboard,
)
from handlers.ui import send_or_update_hub
from utils.i18n import t, resolve_user_lang, text_variants, set_user_language_cached

router = Router()


async def _show_reply_menu(message: Message, lang: str) -> None:
    """
    Гарантированно показывает ReplyKeyboard.
    Важно: только sendMessage реально “включает” ReplyKeyboard,
    editMessageText этого не делает.
    """
    await message.answer(t(lang, "menu.choose_below"), reply_markup=bottom_menu_keyboard(lang))


# ---------------- Commands ----------------

@router.message(CommandStart())
async def cmd_start(message: Message, ui_state):
    lang = await resolve_user_lang(message.from_user.id, message.from_user.language_code)
    await _show_reply_menu(message, lang)
    await send_or_update_hub(message, t(lang, "menu.welcome"), None, ui_state, repost=True)


@router.message(Command("menu"))
async def cmd_menu(message: Message, ui_state):
    lang = await resolve_user_lang(message.from_user.id, message.from_user.language_code)
    await _show_reply_menu(message, lang)
    await send_or_update_hub(message, t(lang, "menu.welcome"), None, ui_state, repost=True)


@router.message(Command("help"))
async def cmd_help(message: Message, ui_state):
    lang = await resolve_user_lang(message.from_user.id, message.from_user.language_code)
    await _show_reply_menu(message, lang)
    await send_or_update_hub(message, t(lang, "menu.help"), None, ui_state, repost=True)


# ---------------- ReplyKeyboard buttons ----------------

@router.message(F.text.in_(text_variants("btn.photos")))
async def btn_photos(message: Message, ui_state):
    lang = await resolve_user_lang(message.from_user.id, message.from_user.language_code)
    await _show_reply_menu(message, lang)
    await send_or_update_hub(
        message,
        t(lang, "menu.photos"),
        photos_menu_keyboard(lang),
        ui_state,
        repost=True,
    )


@router.message(F.text.in_(text_variants("btn.fun")))
async def btn_fun(message: Message, ui_state):
    lang = await resolve_user_lang(message.from_user.id, message.from_user.language_code)
    await _show_reply_menu(message, lang)
    await send_or_update_hub(
        message,
        t(lang, "menu.fun"),
        fun_menu_keyboard(lang),
        ui_state,
        repost=True,
    )


@router.message(F.text.in_(text_variants("btn.useful")))
async def btn_useful(message: Message, ui_state):
    lang = await resolve_user_lang(message.from_user.id, message.from_user.language_code)
    await _show_reply_menu(message, lang)
    await send_or_update_hub(
        message,
        t(lang, "menu.useful"),
        useful_menu_keyboard(lang),
        ui_state,
        repost=True,
    )


@router.message(F.text.in_(text_variants("btn.rate")))
async def btn_survey(message: Message, ui_state):
    lang = await resolve_user_lang(message.from_user.id, message.from_user.language_code)
    await _show_reply_menu(message, lang)
    await send_or_update_hub(
        message,
        t(lang, "menu.survey"),
        survey_keyboard(lang),
        ui_state,
        repost=True,
    )


@router.message(F.text.in_(text_variants("btn.help")))
async def btn_help(message: Message, ui_state):
    lang = await resolve_user_lang(message.from_user.id, message.from_user.language_code)
    await _show_reply_menu(message, lang)
    await send_or_update_hub(message, t(lang, "menu.help"), None, ui_state, repost=True)


@router.message(F.text.in_(text_variants("btn.language")))
async def btn_language(message: Message, ui_state):
    lang = await resolve_user_lang(message.from_user.id, message.from_user.language_code)
    await _show_reply_menu(message, lang)
    await send_or_update_hub(
        message,
        t(lang, "lang.choose"),
        language_keyboard(lang),
        ui_state,
        repost=True,
    )


# ---------------- Inline callbacks (кнопка ⬅️ В меню) ----------------

@router.callback_query(F.data == "menu:main")
async def cb_menu_main(call: CallbackQuery, ui_state):
    # reply keyboard из callback не ставится — это нормально.
    # Пользователь всегда может вернуть клавиатуру командой /menu
    lang = await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    await send_or_update_hub(call.message, t(lang, "menu.welcome"), None, ui_state, repost=True)
    await call.answer()


@router.callback_query(F.data == "menu:photos")
async def cb_menu_photos(call: CallbackQuery, ui_state):
    lang = await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    await send_or_update_hub(
        call.message,
        t(lang, "menu.photos"),
        photos_menu_keyboard(lang),
        ui_state,
        repost=True,
    )
    await call.answer()


@router.callback_query(F.data == "menu:fun")
async def cb_menu_fun(call: CallbackQuery, ui_state):
    lang = await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    await send_or_update_hub(
        call.message,
        t(lang, "menu.fun"),
        fun_menu_keyboard(lang),
        ui_state,
        repost=True,
    )
    await call.answer()


@router.callback_query(F.data == "menu:useful")
async def cb_menu_useful(call: CallbackQuery, ui_state):
    lang = await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    await send_or_update_hub(
        call.message,
        t(lang, "menu.useful"),
        useful_menu_keyboard(lang),
        ui_state,
        repost=True,
    )
    await call.answer()


@router.callback_query(F.data.startswith("lang:set:"))
async def cb_set_language(call: CallbackQuery, ui_state):
    lang = call.data.split(":")[-1]
    await set_user_language_cached(call.from_user.id, lang)
    await _show_reply_menu(call.message, lang)
    await send_or_update_hub(call.message, t(lang, "menu.welcome"), None, ui_state, repost=True)
    await call.answer(t(lang, "lang.updated"))


# ---------------- Fallback ----------------

@router.message(~F.text.in_(text_variants("btn.photos") + text_variants("btn.fun") + text_variants("btn.facts") + text_variants("btn.useful") + text_variants("btn.help") + text_variants("btn.rate") + text_variants("btn.language")))
async def fallback(message: Message):
    # На любое непонятное сообщение — возвращаем клавиатуру
    lang = await resolve_user_lang(message.from_user.id, message.from_user.language_code)
    await _show_reply_menu(message, lang)
    await message.answer(t(lang, "menu.fallback"))
