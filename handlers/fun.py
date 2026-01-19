from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.keyboards import (
    fun_menu_keyboard,
    zodiac_keyboard,
    action_menu_keyboard,
)
from handlers.ui import edit_or_send
from utils.compliments_blanks import random_compliments, generate_horoscope


router = Router()


@router.callback_query(F.data == "fun:compliment")
async def fun_compliment(call: CallbackQuery, ui_state):
    await edit_or_send(
        call,
        f"💖 <b>Комплимент</b>\n────────\n{random_compliments()}",
        action_menu_keyboard("Еще комплимент", "fun:compliment"),
        ui_state,
    )
    await call.answer()


@router.callback_query(F.data == "fun:game")
async def fun_game(call: CallbackQuery, ui_state):
    await edit_or_send(
        call,
        "🎮 <b>Кошачья игра</b>\n"
        "────────\n"
        "Запускай: https://t.me/catizenbot/gameapp?startapp=r_3_2007855",
        action_menu_keyboard("Еще настроение", "menu:fun"),
        ui_state,
    )
    await call.answer()


@router.callback_query(F.data == "fun:horoscope")
async def fun_horoscope(call: CallbackQuery, ui_state):
    await edit_or_send(
        call,
        "🔮 <b>Гороскоп</b>\nВыбери знак зодиака:\n────────",
        zodiac_keyboard(),
        ui_state,
    )
    await call.answer()


@router.callback_query(F.data.startswith("zodiac:"))
async def zodiac_choice(call: CallbackQuery, ui_state):
    await edit_or_send(
        call,
        f"🔮 <b>Твой гороскоп</b>\n────────\n{generate_horoscope()}",
        action_menu_keyboard("Еще гороскоп", "fun:horoscope"),
        ui_state,
    )
    await call.answer()
