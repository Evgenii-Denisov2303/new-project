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
    "Выбери раздел кнопками снизу 👇\n"
    "────────"
)

HELP_TEXT = (
    "ℹ️ <b>Как пользоваться</b>\n"
    "• Нажимай кнопки снизу (меню)\n"
    "• Внутри разделов используй кнопки под сообщениями\n"
    "• Если меню пропало — напиши /menu\n"
    "────────"
)

PHOTOS_TEXT = "📸 <b>Фото котиков</b>\nВыбери любимчика или нажми случайный кадр.\n────────"
FUN_TEXT = "✨ <b>Настроение</b>\nКомплимент, гороскоп, игры.\n────────"
USEFUL_TEXT = "🧼 <b>Уход за котиками</b>\nКороткий, добрый совет.\n────────"
SURVEY_TEXT = "⭐ <b>Оценка</b>\nОцени бота или оставь отзыв.\n────────"


async def _wake_reply_menu(message: Message) -> None:
    """
    ✅ Гарантированно возвращает ReplyKeyboard (нижние кнопки).
    Важно: ReplyKeyboard нельзя надежно вернуть через edit_message_text,
    поэтому мы всегда делаем отдельный sendMessage.
    """
    try:
        await message.answer("\u200b", reply_markup=bottom_menu_keyboard())
    except Exception:
        # если нельзя отправить (редко) — просто игнор
        pass


# ---------------- Commands ----------------

@router.message(CommandStart())
async def start_command(message: Message, ui_state):
    await _wake_reply_menu(message)
    await send_or_update_hub(
        message,
        WELCOME_TEXT,
        None,
        ui_state,
        repost=True,
    )


@router.message(Command("menu"))
async def menu_command(message: Message, ui_state):
    await _wake_reply_menu(message)
    await send_or_update_hub(
        message,
        WELCOME_TEXT,
        None,
        ui_state,
        repost=True,
    )


@router.message(Command("help"))
async def help_command(message: Message, ui_state):
    await _wake_reply_menu(message)
    await send_or_update_hub(
        message,
        HELP_TEXT,
        None,
        ui_state,
        repost=True,
    )


# ---------------- ReplyKeyboard buttons ----------------

@router.message(F.text == "Фото")
async def menu_photos_button(message: Message, ui_state):
    await _wake_reply_menu(message)
    await send_or_update_hub(
        message,
        PHOTOS_TEXT,
        photos_menu_keyboard(),
        ui_state,
        repost=True,
    )


@router.message(F.text == "Настроение")
async def menu_fun_button(message: Message, ui_state):
    await _wake_reply_menu(message)
    await send_or_update_hub(
        message,
        FUN_TEXT,
        fun_menu_keyboard(),
        ui_state,
        repost=True,
    )


@router.message(F.text == "Уход")
async def menu_useful_button(message: Message, ui_state):
    await _wake_reply_menu(message)
    await send_or_update_hub(
        message,
        USEFUL_TEXT,
        useful_menu_keyboard(),
        ui_state,
        repost=True,
    )


@router.message(F.text == "Оценить")
async def menu_survey_button(message: Message, ui_state):
    await _wake_reply_menu(message)
    await send_or_update_hub(
        message,
        SURVEY_TEXT,
        survey_keyboard(),
        ui_state,
        repost=True,
    )


@router.message(F.text == "Помощь")
async def menu_help_button(message: Message, ui_state):
    await _wake_reply_menu(message)
    await send_or_update_hub(
        message,
        HELP_TEXT,
        None,
        ui_state,
        repost=True,
    )


# ---------------- Inline menu callbacks (если они у тебя есть) ----------------

@router.callback_query(F.data == "menu:main")
async def cb_menu_main(call: CallbackQuery, ui_state):
    await send_or_update_hub(call.message, WELCOME_TEXT, None, ui_state, repost=True)
    await call.answer()


@router.callback_query(F.data == "menu:photos")
async def cb_menu_photos(call: CallbackQuery, ui_state):
    await send_or_update_hub(call.message, PHOTOS_TEXT, photos_menu_keyboard(), ui_state, repost=True)
    await call.answer()


@router.callback_query(F.data == "menu:fun")
async def cb_menu_fun(call: CallbackQuery, ui_state):
    await send_or_update_hub(call.message, FUN_TEXT, fun_menu_keyboard(), ui_state, repost=True)
    await call.answer()


@router.callback_query(F.data == "menu:useful")
async def cb_menu_useful(call: CallbackQuery, ui_state):
    await send_or_update_hub(call.message, USEFUL_TEXT, useful_menu_keyboard(), ui_state, repost=True)
    await call.answer()


@router.callback_query(F.data == "menu:help")
async def cb_menu_help(call: CallbackQuery, ui_state):
    await send_or_update_hub(call.message, HELP_TEXT, None, ui_state, repost=True)
    await call.answer()


# ---------------- Fallback: любое сообщение возвращает меню ----------------

@router.message()
async def fallback_message(message: Message):
    # Если пользователь написал что-то непонятное — просто вернём меню
    await _wake_reply_menu(message)
    await message.answer("Нажми кнопку снизу 👇 или напиши /menu")