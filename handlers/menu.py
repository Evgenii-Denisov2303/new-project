from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from handlers.keyboards import (
    photos_menu_keyboard,
    fun_menu_keyboard,
    useful_menu_keyboard,
    survey_keyboard,
    bottom_menu_keyboard,
)
from handlers.ui import send_or_update_hub


router = Router()

WELCOME_TEXT = (
    "🐾 <b>Котик-ботик</b>\n"
    "Выбери раздел кнопками снизу.\n"
    "────────"
)

HELP_TEXT = (
    "ℹ️ <b>Как пользоваться</b>\n"
    "• Нажимай кнопки снизу (меню)\n"
    "• Внутри разделов используй кнопки под сообщениями\n"
    "• Если меню пропало — напиши /menu\n"
    "────────"
)


def _reply_menu():
    return bottom_menu_keyboard()


@router.message(CommandStart())
async def start_command(message: Message, ui_state):
    await send_or_update_hub(
        message,
        WELCOME_TEXT,
        None,
        ui_state,
        reply_keyboard=_reply_menu(),
        repost=True,
    )


@router.message(Command("menu"))
async def menu_command(message: Message, ui_state):
    await send_or_update_hub(
        message,
        WELCOME_TEXT,
        None,
        ui_state,
        reply_keyboard=_reply_menu(),
        repost=True,
    )


@router.message(Command("help"))
async def help_command(message: Message, ui_state):
    await send_or_update_hub(
        message,
        HELP_TEXT,
        None,
        ui_state,
        reply_keyboard=_reply_menu(),
        repost=True,
    )


# ---------- ReplyKeyboard кнопки (снизу) ----------

@router.message(F.text == "Фото")
async def menu_photos_button(message: Message, ui_state):
    await send_or_update_hub(
        message,
        "📸 <b>Фото котиков</b>\nВыбери любимчика или нажми случайный кадр.\n────────",
        photos_menu_keyboard(),
        ui_state,
        reply_keyboard=_reply_menu(),
        repost=True,
    )


@router.message(F.text == "Настроение")
async def menu_fun_button(message: Message, ui_state):
    await send_or_update_hub(
        message,
        "✨ <b>Настроение</b>\nКомплимент, гороскоп, игры.\n────────",
        fun_menu_keyboard(),
        ui_state,
        reply_keyboard=_reply_menu(),
        repost=True,
    )


@router.message(F.text == "Уход")
async def menu_useful_button(message: Message, ui_state):
    await send_or_update_hub(
        message,
        "🧼 <b>Уход за котиками</b>\nКороткий, добрый совет.\n────────",
        useful_menu_keyboard(),
        ui_state,
        reply_keyboard=_reply_menu(),
        repost=True,
    )


@router.message(F.text == "Оценить")
async def menu_survey_button(message: Message, ui_state):
    await send_or_update_hub(
        message,
        "⭐ <b>Оценка</b>\nОцени бота или оставь отзыв.\n────────",
        survey_keyboard(),
        ui_state,
        reply_keyboard=_reply_menu(),
        repost=True,
    )


@router.message(F.text == "Помощь")
async def menu_help_button(message: Message, ui_state):
    await send_or_update_hub(
        message,
        HELP_TEXT,
        None,
        ui_state,
        reply_keyboard=_reply_menu(),
        repost=True,
    )


# ---------- Inline меню переходы ----------

@router.callback_query(F.data == "menu:main")
async def menu_main(call: CallbackQuery, ui_state):
    await send_or_update_hub(call.message, WELCOME_TEXT, None, ui_state, repost=True)
    await call.answer()


@router.callback_query(F.data == "menu:photos")
async def menu_photos(call: CallbackQuery, ui_state):
    await send_or_update_hub(
        call.message,
        "📸 <b>Фото котиков</b>\nВыбери любимчика или нажми случайный кадр.\n────────",
        photos_menu_keyboard(),
        ui_state,
        repost=True,
    )
    await call.answer()


@router.callback_query(F.data == "menu:fun")
async def menu_fun(call: CallbackQuery, ui_state):
    await send_or_update_hub(
        call.message,
        "✨ <b>Настроение</b>\nКомплимент, гороскоп, игры.\n────────",
        fun_menu_keyboard(),
        ui_state,
        repost=True,
    )
    await call.answer()


@router.callback_query(F.data == "menu:useful")
async def menu_useful(call: CallbackQuery, ui_state):
    await send_or_update_hub(
        call.message,
        "🧼 <b>Уход за котиками</b>\nКороткий, добрый совет.\n────────",
        useful_menu_keyboard(),
        ui_state,
        repost=True,
    )
    await call.answer()


@router.callback_query(F.data == "menu:help")
async def menu_help(call: CallbackQuery, ui_state):
    await send_or_update_hub(call.message, HELP_TEXT, None, ui_state, repost=True)
    await call.answer()


# ---------- Fallback: возвращаем клавиатуру если пользователь что-то написал ----------

@router.message()
async def fallback_message(message: Message, ui_state):
    # Если пользователь ввёл произвольный текст — просто возвращаем меню
    await message.answer(
        "Выбери раздел кнопками снизу 👇\n(или напиши /menu)",
        reply_markup=_reply_menu(),
    )