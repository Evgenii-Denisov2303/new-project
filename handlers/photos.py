from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto

from config_data.config import CAT_PHOTOS
from handlers.keyboards import action_menu_keyboard
from handlers.ui import edit_or_send
from services.cat_random_image_api import fetch_random_cat_image
from utils.concurrency import acquire_or_notify


router = Router()


async def _send_local_album(call: CallbackQuery, photo_list, title, ui_state):
    media = [InputMediaPhoto(media=FSInputFile(path)) for path in photo_list]
    await edit_or_send(
        call,
        f"📸 <b>{title}</b>\n────────\nСобираю альбом...",
        action_menu_keyboard("Еще фото", "menu:photos"),
        ui_state,
    )
    await call.bot.send_media_group(chat_id=call.message.chat.id, media=media)
    await edit_or_send(
        call,
        f"📸 <b>{title}</b>\n────────\nГотово. Хочешь еще?",
        action_menu_keyboard("Еще фото", "menu:photos"),
        ui_state,
    )


@router.callback_query(F.data == "photo:manechka")
async def photo_manechka(call: CallbackQuery, ui_state):
    await _send_local_album(call, CAT_PHOTOS["Манечка"], "Манечка", ui_state)
    await call.answer()


@router.callback_query(F.data == "photo:cezar")
async def photo_cezar(call: CallbackQuery, ui_state):
    await _send_local_album(call, CAT_PHOTOS["Цезарь"], "Цезарь", ui_state)
    await call.answer()


@router.callback_query(F.data == "photo:scottish")
async def photo_scottish(call: CallbackQuery, ui_state):
    await _send_local_album(call, CAT_PHOTOS["Шотландец"], "Шотландец", ui_state)
    await call.answer()


@router.callback_query(F.data == "photo:random")
async def photo_random(call: CallbackQuery, session, settings, semaphore, ui_state):
    if not await acquire_or_notify(semaphore, call):
        return
    try:
        await edit_or_send(
            call,
            "🎲 <b>Случайный котик</b>\n────────\nИщу самого пушистого...",
            action_menu_keyboard("🎲 Еще случайный", "photo:random"),
            ui_state,
        )
        image_url = await fetch_random_cat_image(session, settings)
    finally:
        semaphore.release()
    if image_url:
        await call.message.answer_photo(
            image_url,
            caption="Вот тебе котик 🐾",
        )
        await edit_or_send(
            call,
            "🎲 <b>Случайный котик</b>\n────────\nГотово. Еще?",
            action_menu_keyboard("🎲 Еще случайный", "photo:random"),
            ui_state,
        )
    else:
        await edit_or_send(
            call,
            "🎲 <b>Случайный котик</b>\n────────\n"
            "Не удалось получить фото. Попробуй чуть позже.",
            action_menu_keyboard("🎲 Еще случайный", "photo:random"),
            ui_state,
        )
    await call.answer()
