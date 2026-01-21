from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.keyboards import (
    zodiac_keyboard,
    action_menu_keyboard,
    fun_menu_keyboard,
)
from handlers.ui import send_or_update_hub
from utils.compliments_blanks import random_compliments, generate_horoscope


router = Router()

FUN_HUB_TEXT = "✨ <b>Настроение</b>\nХочешь комплимент, гороскоп или игру?\n────────"


@router.callback_query(F.data == "fun:compliment")
async def fun_compliment(call: CallbackQuery, ui_state):
    # Result as a new message (always at the bottom)
    await call.message.answer(
        f"💖 <b>Комплимент</b>\n────────\n{random_compliments()}",
        reply_markup=action_menu_keyboard("Еще комплимент", "fun:compliment"),
    )
    # Repost the section menu below the result, so next click happens at the bottom
    await send_or_update_hub(call.message, FUN_HUB_TEXT, fun_menu_keyboard(), ui_state, repost=True)
    await call.answer()


@router.callback_query(F.data == "fun:game")
async def fun_game(call: CallbackQuery, ui_state):
    await call.message.answer(
        "🎮 <b>Кошачья игра</b>\n"
        "────────\n"
        "Запускай: https://t.me/catizenbot/gameapp?startapp=r_3_2007855",
        reply_markup=action_menu_keyboard("Еще настроение", "menu:fun"),
    )
    await send_or_update_hub(call.message, FUN_HUB_TEXT, fun_menu_keyboard(), ui_state, repost=True)
    await call.answer()


@router.callback_query(F.data == "fun:horoscope")
async def fun_horoscope(call: CallbackQuery, ui_state):
    # Make zodiac selector the hub message (at the bottom)
    await send_or_update_hub(
        call.message,
        "🔮 <b>Гороскоп</b>\nВыбери знак зодиака:\n────────",
        zodiac_keyboard(),
        ui_state,
        repost=True,
    )
    await call.answer()


@router.callback_query(F.data.startswith("zodiac:"))
async def zodiac_choice(call: CallbackQuery, ui_state):
    await call.message.answer(
        f"🔮 <b>Твой гороскоп</b>\n────────\n{generate_horoscope()}",
        reply_markup=action_menu_keyboard("Еще гороскоп", "fun:horoscope"),
    )
    await send_or_update_hub(call.message, FUN_HUB_TEXT, fun_menu_keyboard(), ui_state, repost=True)
    await call.answer()
