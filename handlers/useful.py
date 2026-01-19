from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.keyboards import useful_menu_keyboard
from handlers.ui import edit_or_send


router = Router()


@router.callback_query(F.data == "useful:advice")
async def useful_advice(call: CallbackQuery, ui_state):
    await edit_or_send(
        call,
        "😽 <b>Как гладить котика</b>\n"
        "────────\n"
        "Короткая статья и советы:\n"
        "https://www.feliway.com/ru/Nash-blog/Kak-pravil-no-gladit-koshku/",
        useful_menu_keyboard(),
        ui_state,
    )
    await call.answer()
