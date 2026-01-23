from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from handlers.keyboards import (
    bottom_menu_keyboard,
    photos_menu_keyboard,
    fun_menu_keyboard,
    useful_menu_keyboard,
    survey_keyboard,
)
from handlers.ui import send_or_update_hub

router = Router()

WELCOME_TEXT = (
    "🐾🐾 <b>Котик-ботик</b>\n"
    "Выбери раздел кнопками снизу 👇\n"
    "────────"
)

HELP_TEXT = (
    "ℹ️ <b>Помощь</b>\n"
    "• Нажимай кнопки снизу (Фото/Настроение/Факты/Уход)\n"
    "• Внутри разделов используй кнопки под сообщениями\n"
    "• Если клавиатура пропала — напиши /menu\n"
    "────────"
)


async def _show_reply_menu(message: Message) -> None:
    """
    Гарантированно показывает ReplyKeyboard.
    Важно: только sendMessage реально “включает” ReplyKeyboard,
    editMessageText этого не делает.
    """
    await message.answer("Выбери раздел ниже 👇", reply_markup=bottom_menu_keyboard())


# ---------------- Commands ----------------

@router.message(CommandStart())
async def cmd_start(message: Message, ui_state):
    await _show_reply_menu(message)
    await send_or_update_hub(message, WELCOME_TEXT, None, ui_state, repost=True)


@router.message(Command("menu"))
async def cmd_menu(message: Message, ui_state):
    await _show_reply_menu(message)
    await send_or_update_hub(message, WELCOME_TEXT, None, ui_state, repost=True)


@router.message(Command("help"))
async def cmd_help(message: Message, ui_state):
    await _show_reply_menu(message)
    await send_or_update_hub(message, HELP_TEXT, None, ui_state, repost=True)


# ---------------- ReplyKeyboard buttons ----------------

@router.message(F.text == "Фото")
async def btn_photos(message: Message, ui_state):
    await _show_reply_menu(message)
    await send_or_update_hub(
        message,
        "📸 <b>Фото котиков</b>\nВыбери котика или нажми 🎲 случайный.\n────────",
        photos_menu_keyboard(),
        ui_state,
        repost=True,
    )


@router.message(F.text == "Настроение")
async def btn_fun(message: Message, ui_state):
    await _show_reply_menu(message)
    await send_or_update_hub(
        message,
        "✨ <b>Настроение</b>\nГороскоп, комплимент или мини-игра.\n────────",
        fun_menu_keyboard(),
        ui_state,
        repost=True,
    )


@router.message(F.text == "Уход")
async def btn_useful(message: Message, ui_state):
    await _show_reply_menu(message)
    await send_or_update_hub(
        message,
        "😽 <b>Уход</b>\nСоветы по котикам.\n────────",
        useful_menu_keyboard(),
        ui_state,
        repost=True,
    )


@router.message(F.text == "Оценить")
async def btn_survey(message: Message, ui_state):
    await _show_reply_menu(message)
    await send_or_update_hub(
        message,
        "⭐ <b>Оценить бота</b>\nВыбери действие.\n────────",
        survey_keyboard(),
        ui_state,
        repost=True,
    )


@router.message(F.text == "Помощь")
async def btn_help(message: Message, ui_state):
    await _show_reply_menu(message)
    await send_or_update_hub(message, HELP_TEXT, None, ui_state, repost=True)


# ---------------- Inline callbacks (кнопка ⬅️ В меню) ----------------

@router.callback_query(F.data == "menu:main")
async def cb_menu_main(call: CallbackQuery, ui_state):
    # reply keyboard из callback не ставится — это нормально.
    # Пользователь всегда может вернуть клавиатуру командой /menu
    await send_or_update_hub(call.message, WELCOME_TEXT, None, ui_state, repost=True)
    await call.answer()


@router.callback_query(F.data == "menu:photos")
async def cb_menu_photos(call: CallbackQuery, ui_state):
    await send_or_update_hub(
        call.message,
        "📸 <b>Фото котиков</b>\nВыбери котика или нажми 🎲 случайный.\n────────",
        photos_menu_keyboard(),
        ui_state,
        repost=True,
    )
    await call.answer()


@router.callback_query(F.data == "menu:fun")
async def cb_menu_fun(call: CallbackQuery, ui_state):
    await send_or_update_hub(
        call.message,
        "✨ <b>Настроение</b>\nГороскоп, комплимент или мини-игра.\n────────",
        fun_menu_keyboard(),
        ui_state,
        repost=True,
    )
    await call.answer()


@router.callback_query(F.data == "menu:useful")
async def cb_menu_useful(call: CallbackQuery, ui_state):
    await send_or_update_hub(
        call.message,
        "😽 <b>Уход</b>\nСоветы по котикам.\n────────",
        useful_menu_keyboard(),
        ui_state,
        repost=True,
    )
    await call.answer()


# ---------------- Fallback ----------------

@router.message()
async def fallback(message: Message):
    # На любое непонятное сообщение — возвращаем клавиатуру
    await _show_reply_menu(message)
    await message.answer("Нажми кнопки снизу 👇 или напиши /menu")
