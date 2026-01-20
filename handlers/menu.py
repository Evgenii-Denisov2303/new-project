from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from handlers.keyboards import (
    main_menu_keyboard,
    photos_menu_keyboard,
    fun_menu_keyboard,
    useful_menu_keyboard,
    bottom_menu_keyboard,
    survey_keyboard,
)
from handlers.ui import edit_or_send, send_or_update_hub


router = Router()


WELCOME_TEXT = (
    "🐾 <b>Котик-ботик</b>\n"
    "Теплый уголок с котиками, фактами и настроением.\n\n"
    "────────\n"
    "Выбери раздел, я рядом."
)

HELP_TEXT = (
    "ℹ️ <b>Как пользоваться</b>\n"
    "• выбирай раздел в меню\n"
    "• нажимай кнопки под сообщением\n"
    "• можно получать еще и еще без спама\n\n"
    "────────\n"
    "Если потеряешься — просто жми «В меню»."
)


async def _ensure_bottom_menu(message: Message, reply_menu_users: set):
    if message.from_user.id in reply_menu_users:
        return
    await message.answer("Меню закреплено снизу.", reply_markup=bottom_menu_keyboard())
    reply_menu_users.add(message.from_user.id)


@router.message(CommandStart())
async def start_command(message: Message, ui_state, reply_menu_users):
    await _ensure_bottom_menu(message, reply_menu_users)
    await send_or_update_hub(message, WELCOME_TEXT, main_menu_keyboard(), ui_state)


@router.message(Command("menu"))
async def menu_command(message: Message, ui_state, reply_menu_users):
    await _ensure_bottom_menu(message, reply_menu_users)
    await send_or_update_hub(message, WELCOME_TEXT, main_menu_keyboard(), ui_state)


@router.message(Command("help"))
async def help_command(message: Message, ui_state, reply_menu_users):
    await _ensure_bottom_menu(message, reply_menu_users)
    await send_or_update_hub(message, HELP_TEXT, main_menu_keyboard(), ui_state)


@router.message(F.text == "Фото")
async def menu_photos_button(message: Message, ui_state, reply_menu_users):
    await _ensure_bottom_menu(message, reply_menu_users)
    await send_or_update_hub(
        message,
        "📸 <b>Фото котиков</b>\nВыбери любимчика или нажми случайный кадр.\n────────",
        photos_menu_keyboard(),
        ui_state,
    )


@router.message(F.text == "Настроение")
async def menu_fun_button(message: Message, ui_state, reply_menu_users):
    await _ensure_bottom_menu(message, reply_menu_users)
    await send_or_update_hub(
        message,
        "✨ <b>Настроение</b>\nХочешь комплимент, гороскоп или игру?\n────────",
        fun_menu_keyboard(),
        ui_state,
    )


@router.message(F.text == "Уход")
async def menu_useful_button(message: Message, ui_state, reply_menu_users):
    await _ensure_bottom_menu(message, reply_menu_users)
    await send_or_update_hub(
        message,
        "🧼 <b>Уход за котиками</b>\nКороткий, добрый совет.\n────────",
        useful_menu_keyboard(),
        ui_state,
    )


@router.message(F.text == "Оценить")
async def menu_survey_button(message: Message, ui_state, reply_menu_users):
    await _ensure_bottom_menu(message, reply_menu_users)
    await send_or_update_hub(
        message,
        "⭐ <b>Оценка</b>\n────────\nОцени бота или оставь отзыв.",
        survey_keyboard(),
        ui_state,
    )


@router.message(F.text == "Помощь")
async def menu_help_button(message: Message, ui_state, reply_menu_users):
    await _ensure_bottom_menu(message, reply_menu_users)
    await send_or_update_hub(message, HELP_TEXT, main_menu_keyboard(), ui_state)


@router.message()
async def fallback_message(message: Message, ui_state, reply_menu_users):
    await _ensure_bottom_menu(message, reply_menu_users)
    await send_or_update_hub(
        message,
        "Я тут, но лучше выбрать раздел в меню 🙂",
        main_menu_keyboard(),
        ui_state,
    )


@router.callback_query(F.data == "menu:main")
async def menu_main(call: CallbackQuery, ui_state):
    await edit_or_send(call, WELCOME_TEXT, main_menu_keyboard(), ui_state)
    await call.answer()


@router.callback_query(F.data == "menu:help")
async def menu_help(call: CallbackQuery, ui_state):
    await edit_or_send(call, HELP_TEXT, main_menu_keyboard(), ui_state)
    await call.answer()


@router.callback_query(F.data == "menu:photos")
async def menu_photos(call: CallbackQuery, ui_state):
    await edit_or_send(
        call,
        "📸 <b>Фото котиков</b>\nВыбери любимчика или нажми случайный кадр.\n────────",
        photos_menu_keyboard(),
        ui_state,
    )
    await call.answer()


@router.callback_query(F.data == "menu:fun")
async def menu_fun(call: CallbackQuery, ui_state):
    await edit_or_send(
        call,
        "✨ <b>Настроение</b>\nХочешь комплимент, гороскоп или игру?\n────────",
        fun_menu_keyboard(),
        ui_state,
    )
    await call.answer()


@router.callback_query(F.data == "menu:useful")
async def menu_useful(call: CallbackQuery, ui_state):
    await edit_or_send(
        call,
        "🧼 <b>Уход за котиками</b>\nКороткий, добрый совет.\n────────",
        useful_menu_keyboard(),
        ui_state,
    )
    await call.answer()
