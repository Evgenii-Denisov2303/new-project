from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.keyboards import action_menu_keyboard
from utils.i18n import t, resolve_user_lang


router = Router()


@router.callback_query(F.data == "useful:advice")
async def useful_advice(call: CallbackQuery):
    lang = await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    await call.message.answer(
        t(lang, "useful.text"),
        reply_markup=action_menu_keyboard(
            t(lang, "btn.more_useful"),
            "useful:advice",
            include_menu=False,
            lang=lang,
        ),
    )
    await call.answer()
