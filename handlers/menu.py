from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from handlers.keyboards import (
    main_menu_keyboard,
    photos_menu_keyboard,
    fun_menu_keyboard,
    useful_menu_keyboard,
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


@router.message(CommandStart())
async def start_command(message: Message, ui_state):
    await send_or_update_hub(message, WELCOME_TEXT, main_menu_keyboard(), ui_state)


@router.message(Command("menu"))
async def menu_command(message: Message, ui_state):
    await send_or_update_hub(message, WELCOME_TEXT, main_menu_keyboard(), ui_state)


@router.message(Command("help"))
async def help_command(message: Message, ui_state):
    await send_or_update_hub(message, HELP_TEXT, main_menu_keyboard(), ui_state)


@router.message()
async def fallback_message(message: Message, ui_state):
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
