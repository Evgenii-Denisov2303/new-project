from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.keyboards import (
    zodiac_keyboard,
    action_menu_keyboard,
    fun_menu_keyboard,
)
from handlers.ui import send_or_update_hub
from utils.compliments_blanks import random_compliments, generate_horoscope
from utils.i18n import t, resolve_user_lang


router = Router()


@router.callback_query(F.data == "fun:compliment")
async def fun_compliment(call: CallbackQuery, ui_state):
    lang = await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    # Result as a new message (always at the bottom)
    await call.message.answer(
        t(lang, "fun.compliment_title").format(value=random_compliments(lang)),
        reply_markup=action_menu_keyboard(t(lang, "btn.more_compliment"), "fun:compliment", lang=lang),
    )
    # Repost the section menu below the result, so next click happens at the bottom
    await send_or_update_hub(call.message, t(lang, "fun.hub"), fun_menu_keyboard(lang), ui_state, repost=True)
    await call.answer()


@router.callback_query(F.data == "fun:game")
async def fun_game(call: CallbackQuery, ui_state):
    lang = await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    await call.message.answer(
        t(lang, "fun.game_title").format(url="https://t.me/catizenbot/gameapp?startapp=r_3_2007855"),
        reply_markup=action_menu_keyboard(t(lang, "btn.more_fun"), "menu:fun", lang=lang),
    )
    await send_or_update_hub(call.message, t(lang, "fun.hub"), fun_menu_keyboard(lang), ui_state, repost=True)
    await call.answer()


@router.callback_query(F.data == "fun:horoscope")
async def fun_horoscope(call: CallbackQuery, ui_state):
    lang = await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    # Make zodiac selector the hub message (at the bottom)
    await send_or_update_hub(
        call.message,
        t(lang, "fun.horoscope_choose"),
        zodiac_keyboard(lang),
        ui_state,
        repost=True,
    )
    await call.answer()


@router.callback_query(F.data.startswith("zodiac:"))
async def zodiac_choice(call: CallbackQuery, ui_state):
    lang = await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    await call.message.answer(
        t(lang, "fun.horoscope_result").format(value=generate_horoscope(lang)),
        reply_markup=action_menu_keyboard(t(lang, "btn.more_horoscope"), "fun:horoscope", lang=lang),
    )
    await send_or_update_hub(call.message, t(lang, "fun.hub"), fun_menu_keyboard(lang), ui_state, repost=True)
    await call.answer()
